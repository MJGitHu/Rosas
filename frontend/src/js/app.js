/**
 * Rosas de Guadalupe Management System - Lógica de Interfaz y Cotizaciones
 */

document.addEventListener("DOMContentLoaded", () => {
  const formatSelect = document.getElementById("format-select");
  const durationInput = document.getElementById("duration-input");
  const durationSelect = document.getElementById("duration-select");
  const quoteForm = document.getElementById("quote-form");
  const eventDateInput = document.getElementById("event-date");
  const financialSummary = document.getElementById("financial-summary");
  const contractSummary = document.getElementById("contract-summary");
  const summaryHeading = document.getElementById("summary-heading");
  const summaryBadge = document.getElementById("summary-badge");
  const qrPaymentSection = document.getElementById("qr-payment-section");
  const contractStatus = document.getElementById("contract-status");
  const btnSaveCashContract = document.getElementById("btn-save-cash-contract");
  const btnBackToQuote = document.getElementById("btn-back-to-quote");
  const paymentCards = document.querySelectorAll(".payment-card");
  const btnRecalculate = document.getElementById("btn-recalculate");
  const btnProceed = document.getElementById("btn-proceed-booking");
  const apiStatusBadge = document.getElementById("api-status-badge");
  const adminSessionButton = document.getElementById("admin-session-button");
  const adminDashboard = document.getElementById("admin-dashboard");
  const adminLoginDialog = document.getElementById("admin-login-dialog");
  const adminLoginForm = document.getElementById("admin-login-form");
  const adminLoginStatus = document.getElementById("admin-login-status");
  const adminCalendarStatus = document.getElementById("admin-calendar-status");
  const calendarGrid = document.getElementById("calendar-grid");
  const calendarMonthLabel = document.getElementById("calendar-month-label");
  const adminContractDetails = document.getElementById("admin-contract-details");
  let adminCsrfToken = "";
  let calendarMonth = new Date(new Date().getFullYear(), new Date().getMonth(), 1);
  let adminReservations = [];

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

  const updateMinimumEventDate = () => {
    const today = new Date();
    const minimumDate = [
      today.getFullYear(),
      String(today.getMonth() + 1).padStart(2, "0"),
      String(today.getDate()).padStart(2, "0"),
    ].join("-");

    eventDateInput.min = minimumDate;
    if (eventDateInput.value && eventDateInput.value < minimumDate) {
      eventDateInput.value = "";
    }
  };

  // Manejo de selección de método de pago
  paymentCards.forEach((card) => {
    card.addEventListener("click", () => {
      if (!contractSummary.hidden) return;
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

  const paymentLabels = {
    TRANSFERENCIA: "Transferencia bancaria",
    TARJETA_CREDITO: "Tarjeta",
    EFECTIVO: "Efectivo",
  };

  const formatDuration = (minutes) => {
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    const parts = [];
    if (hours) parts.push(`${hours} ${hours === 1 ? "hora" : "horas"}`);
    if (remainingMinutes) parts.push(`${remainingMinutes} minutos`);
    return parts.join(" y ");
  };

  const showContractSummary = () => {
    const selectedFormat = formatSelect.options[formatSelect.selectedIndex];
    const additionalHours = parseInt(durationInput.value, 10) || 0;
    const totalMinutes = parseInt(durationSelect.value, 10) + additionalHours * 60;
    const paymentMethod = getSelectedPaymentMethod();
    const clientName = [
      document.getElementById("client-first-name").value.trim(),
      document.getElementById("client-last-name").value.trim(),
    ].join(" ");
    const [year, month, day] = eventDateInput.value.split("-").map(Number);
    const eventDate = new Date(year, month - 1, day).toLocaleDateString("es-PE", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });

    document.getElementById("contract-client").textContent = clientName;
    document.getElementById("contract-contact").textContent =
      `${document.getElementById("client-phone").value.trim()} · ${document.getElementById("client-email").value.trim()}`;
    document.getElementById("contract-service").textContent = selectedFormat.textContent.trim();
    document.getElementById("contract-duration").textContent = formatDuration(totalMinutes);
    document.getElementById("contract-address").textContent =
      document.getElementById("event-address").value.trim();
    document.getElementById("contract-datetime").textContent =
      `${eventDate} · ${document.getElementById("event-time").value}`;
    document.getElementById("contract-notes").textContent =
      document.getElementById("details-input").value.trim() || "Sin detalles adicionales";
    document.getElementById("contract-payment").textContent = paymentLabels[paymentMethod];
    document.getElementById("contract-total").textContent =
      summaryTotal.textContent;
    document.getElementById("contract-advance").textContent =
      `${summaryAdvance.textContent} (anticipo requerido)`;
    document.getElementById("contract-fee").textContent = summaryFee.textContent;
    document.getElementById("contract-pay-now").textContent = summaryPayNow.textContent;
    document.getElementById("contract-balance").textContent =
      summaryBalance.textContent;

    const usesElectronicPayment = paymentMethod !== "EFECTIVO";
    qrPaymentSection.hidden = !usesElectronicPayment;
    btnSaveCashContract.hidden = usesElectronicPayment;
    contractStatus.hidden = true;
    contractStatus.textContent = "";
    btnSaveCashContract.disabled = false;
    btnSaveCashContract.textContent = "Continuar";
    btnBackToQuote.hidden = false;
    Array.from(quoteForm.elements).forEach((control) => {
      control.disabled = true;
    });

    summaryHeading.textContent = "Resumen del contrato";
    summaryBadge.textContent = paymentLabels[paymentMethod];
    financialSummary.hidden = true;
    contractSummary.hidden = false;
  };

  // Cálculo de cotización (con fallback local o vía API Flask)
  const calculateQuote = async () => {
    const selectedFormat = formatSelect.options[formatSelect.selectedIndex];
    const selectedDuration = durationSelect.value;
    const basePrice = parseFloat(selectedFormat.getAttribute(`data-price-${selectedDuration}`));
    const oneHourPrice = parseFloat(selectedFormat.getAttribute("data-price-60"));
    const requestedAdditionalHours = parseInt(durationInput.value, 10);
    const additionalHours = Number.isFinite(requestedAdditionalHours)
      ? Math.min(6, Math.max(0, requestedAdditionalHours))
      : 0;
    if (durationInput.value !== String(additionalHours)) {
      durationInput.value = additionalHours;
    }
    const durationHours = parseInt(selectedDuration, 10) / 60 + additionalHours;
    const additionalDurationCharge = additionalHours * (oneHourPrice - 60);
    const zoneSurcharge = 0;
    const paymentMethod = getSelectedPaymentMethod();

    // Intentar consultar endpoint del backend Flask
    try {
      const response = await fetch("/api/cotizaciones/calcular", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          precio_base_hora: basePrice,
          duracion_horas: durationHours,
          monto_base_formato: basePrice,
          recargo_duracion: additionalDurationCharge,
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
    const subtotal = basePrice + additionalDurationCharge;
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
      const res = await fetch("/api/health");
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

  const setAdminMode = (enabled) => {
    document.getElementById("informacion").hidden = enabled;
    document.querySelector(".booking-section").hidden = enabled;
    adminDashboard.hidden = !enabled;
    adminSessionButton.textContent = enabled
      ? "Cerrar sesión"
      : "Sesión de administración";
    adminSessionButton.setAttribute(
      "aria-label",
      enabled ? "Cerrar sesión de administración" : "Iniciar sesión de administración"
    );
    if (!enabled) {
      adminContractDetails.hidden = true;
    }
  };

  const displayAdminStatus = (message, isError = false) => {
    adminCalendarStatus.textContent = message;
    adminCalendarStatus.classList.toggle("error", isError);
    adminCalendarStatus.hidden = !message;
  };

  const apiMessage = async (response, fallbackMessage) => {
    const result = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(result.message || fallbackMessage);
    }
    return result;
  };

  const monthKey = (date) =>
    `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}`;

  const showReservationDetails = (reservation) => {
    const fullName = `${reservation.nombre} ${reservation.apellido}`.trim();
    const [year, month, day] = reservation.fecha_evento.split("-").map(Number);
    const formattedDate = new Date(year, month - 1, day).toLocaleDateString("es-PE", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
    const durationMinutes = Math.round(reservation.duracion_horas * 60);
    const detailValues = {
      "admin-detail-code": reservation.codigo_reserva,
      "admin-detail-client": fullName,
      "admin-detail-contact": `${reservation.telefono} · ${reservation.email}`,
      "admin-detail-service": reservation.formato,
      "admin-detail-datetime": `${formattedDate} · ${reservation.hora_inicio}`,
      "admin-detail-address": reservation.direccion_evento,
      "admin-detail-type": reservation.tipo_evento || "No especificado",
      "admin-detail-status": reservation.estado,
      "admin-detail-duration": formatDuration(durationMinutes),
      "admin-detail-payment": paymentLabels[reservation.metodo_pago] || reservation.metodo_pago,
      "admin-detail-subtotal": formatearSoles(reservation.subtotal),
      "admin-detail-surcharge": formatearSoles(reservation.recargo),
      "admin-detail-total": formatearSoles(reservation.total),
      "admin-detail-advance": formatearSoles(reservation.anticipo),
      "admin-detail-balance": formatearSoles(reservation.saldo_pendiente),
      "admin-detail-notes": reservation.detalles || "Sin detalles adicionales",
    };
    Object.entries(detailValues).forEach(([id, value]) => {
      document.getElementById(id).textContent = value ?? "—";
    });
    adminContractDetails.hidden = false;
  };

  const renderCalendar = () => {
    calendarMonthLabel.textContent = calendarMonth.toLocaleDateString("es-PE", {
      month: "long",
      year: "numeric",
    });
    calendarGrid.replaceChildren();
    const firstWeekday = (calendarMonth.getDay() + 6) % 7;
    const start = new Date(
      calendarMonth.getFullYear(),
      calendarMonth.getMonth(),
      1 - firstWeekday
    );
    const eventsByDate = new Map();
    adminReservations.forEach((reservation) => {
      if (!eventsByDate.has(reservation.fecha_evento)) {
        eventsByDate.set(reservation.fecha_evento, []);
      }
      eventsByDate.get(reservation.fecha_evento).push(reservation);
    });

    for (let index = 0; index < 42; index += 1) {
      const day = new Date(start.getFullYear(), start.getMonth(), start.getDate() + index);
      const dateKey = [
        day.getFullYear(),
        String(day.getMonth() + 1).padStart(2, "0"),
        String(day.getDate()).padStart(2, "0"),
      ].join("-");
      const cell = document.createElement("div");
      cell.className = "calendar-day";
      if (day.getMonth() !== calendarMonth.getMonth()) {
        cell.classList.add("outside-month");
      }
      const number = document.createElement("span");
      number.className = "calendar-day-number";
      number.textContent = String(day.getDate());
      cell.append(number);

      (eventsByDate.get(dateKey) || []).forEach((reservation) => {
        const eventButton = document.createElement("button");
        eventButton.type = "button";
        eventButton.className = "calendar-event";
        eventButton.textContent =
          `${reservation.hora_inicio} · ${reservation.nombre} ${reservation.apellido}`;
        eventButton.title = `${reservation.codigo_reserva}: ${reservation.nombre} ${reservation.apellido}`;
        eventButton.addEventListener("click", () => showReservationDetails(reservation));
        cell.append(eventButton);
      });
      calendarGrid.append(cell);
    }
  };

  const loadCalendar = async () => {
    displayAdminStatus("Cargando contratos...");
    calendarGrid.setAttribute("aria-busy", "true");
    adminContractDetails.hidden = true;
    try {
      const response = await fetch(`/api/admin/reservas?mes=${monthKey(calendarMonth)}`, {
        credentials: "same-origin",
      });
      const result = await apiMessage(response, "No se pudo cargar el calendario.");
      adminReservations = result.data;
      renderCalendar();
      displayAdminStatus(
        adminReservations.length
          ? `${adminReservations.length} contrato(s) en este mes.`
          : "No hay contratos agendados en este mes."
      );
    } catch (error) {
      adminReservations = [];
      renderCalendar();
      displayAdminStatus(error.message, true);
    } finally {
      calendarGrid.removeAttribute("aria-busy");
    }
  };

  const synchronizeAdminSession = async () => {
    try {
      const response = await fetch("/api/admin/session", { credentials: "same-origin" });
      const result = await apiMessage(response, "No se pudo verificar la sesión.");
      if (result.authenticated) {
        adminCsrfToken = result.csrf_token;
        setAdminMode(true);
        await loadCalendar();
      }
    } catch (error) {
      displayAdminStatus(error.message, true);
    }
  };

  adminSessionButton.addEventListener("click", async () => {
    if (!adminDashboard.hidden) {
      try {
        const response = await fetch("/api/admin/logout", {
          method: "POST",
          credentials: "same-origin",
          headers: { "X-CSRF-Token": adminCsrfToken },
        });
        await apiMessage(response, "No se pudo cerrar la sesión.");
        adminCsrfToken = "";
        setAdminMode(false);
      } catch (error) {
        displayAdminStatus(error.message, true);
      }
      return;
    }
    adminLoginStatus.hidden = true;
    adminLoginStatus.textContent = "";
    adminLoginForm.reset();
    adminLoginDialog.showModal();
  });

  document.getElementById("admin-login-cancel").addEventListener("click", () => {
    adminLoginDialog.close();
  });

  adminLoginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const submitButton = document.getElementById("admin-login-submit");
    submitButton.disabled = true;
    adminLoginStatus.hidden = true;
    try {
      const response = await fetch("/api/admin/login", {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: document.getElementById("admin-username").value,
          password: document.getElementById("admin-password").value,
        }),
      });
      const result = await apiMessage(response, "No se pudo iniciar sesión.");
      adminCsrfToken = result.csrf_token;
      adminLoginDialog.close();
      setAdminMode(true);
      await loadCalendar();
    } catch (error) {
      adminLoginStatus.textContent = error.message;
      adminLoginStatus.hidden = false;
    } finally {
      submitButton.disabled = false;
      document.getElementById("admin-password").value = "";
    }
  });

  document.getElementById("calendar-previous").addEventListener("click", () => {
    calendarMonth = new Date(calendarMonth.getFullYear(), calendarMonth.getMonth() - 1, 1);
    loadCalendar();
  });

  document.getElementById("calendar-next").addEventListener("click", () => {
    calendarMonth = new Date(calendarMonth.getFullYear(), calendarMonth.getMonth() + 1, 1);
    loadCalendar();
  });

  // Event Listeners
  formatSelect.addEventListener("change", calculateQuote);
  durationSelect.addEventListener("change", calculateQuote);
  durationInput.addEventListener("input", calculateQuote);
  btnRecalculate.addEventListener("click", calculateQuote);

  btnProceed.addEventListener("click", () => {
    updateMinimumEventDate();
    if (!quoteForm.reportValidity()) return;
    showContractSummary();
  });

  btnBackToQuote.addEventListener("click", () => {
    contractSummary.hidden = true;
    financialSummary.hidden = false;
    summaryHeading.textContent = "Desglose Financiero de Contratación";
    summaryBadge.textContent = "Política 50/50";
    Array.from(quoteForm.elements).forEach((control) => {
      control.disabled = false;
    });
  });

  btnSaveCashContract.addEventListener("click", async () => {
    btnSaveCashContract.disabled = true;
    btnSaveCashContract.textContent = "Guardando...";
    contractStatus.hidden = true;
    contractStatus.textContent = "";

    try {
      const response = await fetch("/api/reservas/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cliente: {
            nombre: document.getElementById("client-first-name").value.trim(),
            apellido: document.getElementById("client-last-name").value.trim(),
            telefono: document.getElementById("client-phone").value.trim(),
            email: document.getElementById("client-email").value.trim(),
          },
          servicio: formatSelect.value,
          duracion_minutos: parseInt(durationSelect.value, 10),
          horas_adicionales: parseInt(durationInput.value, 10) || 0,
          direccion_evento: document.getElementById("event-address").value.trim(),
          fecha_evento: eventDateInput.value,
          hora_evento: document.getElementById("event-time").value,
          detalles: document.getElementById("details-input").value.trim(),
          metodo_pago: getSelectedPaymentMethod(),
        }),
      });
      const result = await response.json();
      if (!response.ok) {
        throw new Error(result.message || "No se pudo guardar el contrato.");
      }

      contractStatus.textContent =
        `Contrato guardado. Código de reserva: ${result.data.codigo_reserva}.`;
      contractStatus.hidden = false;
      btnSaveCashContract.textContent = "Contrato guardado";
      btnBackToQuote.hidden = true;
    } catch (error) {
      contractStatus.textContent =
        `No se pudo guardar el contrato: ${error.message}`;
      contractStatus.hidden = false;
      btnSaveCashContract.disabled = false;
      btnSaveCashContract.textContent = "Reintentar";
    }
  });

  // Inicialización
  updateMinimumEventDate();
  eventDateInput.addEventListener("focus", updateMinimumEventDate);
  calculateQuote();
  checkBackendHealth();
  synchronizeAdminSession();
});
