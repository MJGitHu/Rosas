/**
 * Rosas de Guadalupe Management System - Lógica de Interfaz y Cotizaciones
 */

document.addEventListener("DOMContentLoaded", () => {
  const formatSelect = document.getElementById("format-select");
  const durationInput = document.getElementById("duration-input");
  const zoneSelect = document.getElementById("zone-select");
  const paymentCards = document.querySelectorAll(".payment-card");
  const btnRecalculate = document.getElementById("btn-recalculate");
  const btnProceed = document.getElementById("btn-proceed-booking");
  const apiStatusBadge = document.getElementById("api-status-badge");

  // Campos de desglose
  const summarySubtotal = document.getElementById("summary-subtotal");
  const summaryLogistics = document.getElementById("summary-logistics");
  const summaryTotal = document.getElementById("summary-total");
  const summaryAdvance = document.getElementById("summary-advance");
  const summaryFee = document.getElementById("summary-fee");
  const summaryPayNow = document.getElementById("summary-pay-now");
  const summaryBalance = document.getElementById("summary-balance");

  const formatearSoles = (monto) => new Intl.NumberFormat('es-PE', {
    style: 'currency',
    currency: 'PEN',
    minimumFractionDigits: 2
  }).format(monto);

  // Manejo de selección de método de pago
  paymentCards.forEach((card) => {
    card.addEventListener("click", () => {
      paymentCards.forEach((c) => c.classList.remove("selected"));
      card.classList.add("selected");
      const radio = card.querySelector('input[type="radio"]');
      if (radio) radio.checked = true;
      calculateQuote();
    });
  });

  const getSelectedPaymentMethod = () => {
    const checked = document.querySelector('input[name="payment-method"]:checked');
    return checked ? checked.value : "TRANSFERENCIA";
  };

  // Cálculo de cotización (con fallback local o vía API Flask)
  const calculateQuote = async () => {
    const basePrice = parseFloat(formatSelect.value) || 2800;
    const duration = parseFloat(durationInput.value) || 1;
    const zoneSurcharge = parseFloat(zoneSelect.value) || 0;
    const paymentMethod = getSelectedPaymentMethod();

    // Intentar consultar endpoint del backend Flask
    try {
      const response = await fetch("http://localhost:5000/api/cotizaciones/calcular", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          precio_base_hora: basePrice,
          duracion_horas: duration,
          recargo_zona: zoneSurcharge,
          metodo_pago: paymentMethod,
        }),
      });

      if (response.ok) {
        const resData = await response.json();
        const data = resData.data;
        updateUI(
          data.subtotal_musical,
          data.recargo_logistica_zona,
          data.monto_total_evento,
          data.anticipo_50_requerido,
          data.comision_pasarela,
          data.total_a_pagar_hoy,
          data.saldo_50_restante
        );
        return;
      }
    } catch (e) {
      // Backend no disponible aún o trabajando en modo local
    }

    // Cálculo reactivo en el navegador
    const subtotal = basePrice * duration;
    const total = subtotal + zoneSurcharge;
    const advance = Math.round(total * 0.5 * 100) / 100;
    const balance = total - advance;

    let fee = 0;
    if (paymentMethod === "TARJETA_CREDITO" || paymentMethod === "TARJETA_DEBITO") {
      fee = Math.round(advance * 0.05 * 100) / 100;
    }

    const payNow = advance + fee;

    updateUI(subtotal, zoneSurcharge, total, advance, fee, payNow, balance);
  };

  const updateUI = (subtotal, logistics, total, advance, fee, payNow, balance) => {
    summarySubtotal.textContent = formatearSoles(subtotal);
    summaryLogistics.textContent = formatearSoles(logistics);
    summaryTotal.textContent = formatearSoles(total);
    summaryAdvance.textContent = formatearSoles(advance);
    summaryFee.textContent = formatearSoles(fee);
    summaryPayNow.textContent = formatearSoles(payNow);
    summaryBalance.textContent = formatearSoles(balance);
  };

  // Verificación de estado del Backend Flask
  const checkBackendHealth = async () => {
    try {
      const res = await fetch("http://localhost:5000/api/health");
      if (res.ok) {
        apiStatusBadge.textContent = "Backend: Conectado (Flask)";
        apiStatusBadge.className = "badge badge-api";
      } else {
        throw new Error();
      }
    } catch {
      apiStatusBadge.textContent = "Backend: Modo Offline / Standalone";
      apiStatusBadge.style.color = "#AD1457";
      apiStatusBadge.style.borderColor = "rgba(194, 24, 91, 0.35)";
    }
  };

  // Event Listeners
  formatSelect.addEventListener("change", calculateQuote);
  durationInput.addEventListener("input", calculateQuote);
  zoneSelect.addEventListener("change", calculateQuote);
  btnRecalculate.addEventListener("click", calculateQuote);

  btnProceed.addEventListener("click", () => {
    alert("¡Excelente! Procediendo a la captura de datos del anfitrión y dirección del evento.");
  });

  // Inicialización
  calculateQuote();
  checkBackendHealth();
});
