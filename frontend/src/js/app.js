/**
 * Rosas de Guadalupe Management System - Lógica de Interfaz y Cotizaciones
 */

document.addEventListener("DOMContentLoaded", () => {
  const formatSelect = document.getElementById("format-select");
  const durationSelect = document.getElementById("duration-select");
  const quoteForm = document.getElementById("quote-form");
  const eventDateInput = document.getElementById("event-date");
  const eventTimeInput = document.getElementById("event-time");
  const eventAvailabilityStatus = document.getElementById("event-availability-status");
  const financialSummary = document.getElementById("financial-summary");
  const contractSummary = document.getElementById("contract-summary");
  const summaryHeading = document.getElementById("summary-heading");
  const summaryBadge = document.getElementById("summary-badge");
  const qrPaymentSection = document.getElementById("qr-payment-section");
  const contractStatus = document.getElementById("contract-status");
  const btnPayContract = document.getElementById("btn-pay-contract");
  const paymentReturnStatus = document.getElementById("payment-return-status");
  const paymentRetryLink = document.getElementById("payment-retry-link");
  const btnBackToQuote = document.getElementById("btn-back-to-quote");
  const paymentCards = document.querySelectorAll(".payment-card");
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
  let availabilityRequestId = 0;

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

  const populateEventTimes = () => {
    for (let minutes = 11 * 60; minutes <= 25 * 60; minutes += 5) {
      const normalizedMinutes = minutes % (24 * 60);
      const hour = Math.floor(normalizedMinutes / 60);
      const minute = normalizedMinutes % 60;
      const value = `${String(hour).padStart(2, "0")}:${String(minute).padStart(2, "0")}`;
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      eventTimeInput.append(option);
    }
  };

  const checkScheduleAvailability = async () => {
    const requestId = ++availabilityRequestId;
    const selectedTime = eventTimeInput.value;
    const selectedDate = eventDateInput.value;
    if (!selectedDate || !selectedTime) {
      eventAvailabilityStatus.hidden = true;
      return false;
    }

    eventAvailabilityStatus.textContent = "Comprobando disponibilidad...";
    eventAvailabilityStatus.className = "schedule-status";
    eventAvailabilityStatus.hidden = false;
    try {
      const parameters = new URLSearchParams({
        fecha: selectedDate,
        hora: selectedTime,
        duracion_minutos: durationSelect.value,
      });
      const response = await fetch(`/api/reservas/disponibilidad?${parameters}`);
      const result = await response.json();
      if (!response.ok) {
        throw new Error(result.message || "No se pudo comprobar la disponibilidad.");
      }
      if (requestId !== availabilityRequestId) return false;
      eventAvailabilityStatus.textContent = result.message;
      eventAvailabilityStatus.classList.toggle("unavailable", !result.available);
      return result.available;
    } catch (error) {
      if (requestId === availabilityRequestId) {
        eventAvailabilityStatus.textContent = error.message;
        eventAvailabilityStatus.classList.add("unavailable");
      }
      return false;
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
    return checked ? checked.value : "MERCADOPAGO";
  };

  const paymentLabels = {
    MERCADOPAGO: "Mercado Pago",
    PRUEBA: "Prueba (S/ 1.00)",
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
    const totalMinutes = parseInt(durationSelect.value, 10);
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
      paymentMethod === "PRUEBA"
        ? `${summaryAdvance.textContent} (pago total de prueba)`
        : `${summaryAdvance.textContent} (anticipo requerido)`;
    document.getElementById("contract-fee").textContent = summaryFee.textContent;
    document.getElementById("contract-pay-now").textContent = summaryPayNow.textContent;
    document.getElementById("contract-balance").textContent =
      summaryBalance.textContent;

    qrPaymentSection.hidden = false;
    contractStatus.hidden = true;
    contractStatus.textContent = "";
    btnPayContract.disabled = false;
    btnPayContract.textContent = paymentMethod === "PRUEBA"
      ? "Pagar S/ 1.00"
      : "Pagar con Mercado Pago";
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
    const zoneSurcharge = 0;
    const paymentMethod = getSelectedPaymentMethod();
    if (paymentMethod === "PRUEBA") {
      updateUI(1, 0, 1, 1, 0, 1, 0);
      return;
    }

    // Intentar consultar endpoint del backend Flask
    try {
      const response = await fetch("/api/cotizaciones/calcular", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          precio_base_hora: basePrice,
          duracion_horas: parseInt(selectedDuration, 10) / 60,
          monto_base_formato: basePrice,
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
    const subtotal = basePrice;
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
    const isTestPayment = getSelectedPaymentMethod() === "PRUEBA";
    document.getElementById("summary-advance-label").textContent = isTestPayment
      ? "Pago total de prueba:"
      : "Anticipo para Bloqueo de Fecha (50%):";
    document.getElementById("summary-balance-label").textContent = isTestPayment
      ? "Saldo pendiente:"
      : "Saldo Pendiente al Llegar al Evento (50%):";
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

  btnProceed.addEventListener("click", async () => {
    updateMinimumEventDate();
    if (!quoteForm.reportValidity()) return;
    if (!(await checkScheduleAvailability())) return;
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

  btnPayContract.addEventListener("click", async () => {
    btnPayContract.disabled = true;
    btnPayContract.textContent = "Conectando con Mercado Pago...";
    contractStatus.hidden = true;
    contractStatus.textContent = "";

    try {
      const response = await fetch("/api/pagos/preferencias", {
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
          direccion_evento: document.getElementById("event-address").value.trim(),
          fecha_evento: eventDateInput.value,
          hora_evento: eventTimeInput.value,
          detalles: document.getElementById("details-input").value.trim(),
          metodo_pago: getSelectedPaymentMethod(),
        }),
      });
      const result = await response.json();
      if (!response.ok) {
        throw new Error(result.message || "No se pudo iniciar el pago.");
      }

      window.location.assign(result.data.init_point);
    } catch (error) {
      contractStatus.textContent =
        `No se pudo iniciar el pago: ${error.message}`;
      contractStatus.hidden = false;
      btnPayContract.disabled = false;
      btnPayContract.textContent = getSelectedPaymentMethod() === "PRUEBA"
        ? "Reintentar pago de S/ 1.00"
        : "Reintentar pago con Mercado Pago";
    }
  });

  const checkReturnedPayment = async () => {
    const parameters = new URLSearchParams(window.location.search);
    const externalReference = parameters.get("external_reference");
    if (parameters.get("payment_return") !== "1" || !externalReference) return;

    paymentRetryLink.hidden = true;
    paymentReturnStatus.hidden = false;
    paymentReturnStatus.textContent = "Verificando el pago con el servidor...";
    const deadline = Date.now() + 60_000;
    while (Date.now() < deadline) {
      try {
        const query = new URLSearchParams({ referencia_externa: externalReference });
        const response = await fetch(`/api/pagos/estado?${query}`);
        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.message || "No se pudo verificar el pago.");
        }
        const payment = result.data;
        if (payment.estado === "APROBADO") {
          paymentReturnStatus.textContent =
            `Pago confirmado. Tu contrato quedó reservado. Código: ${payment.codigo_reserva}.`;
          return;
        }
        if (payment.estado === "RECHAZADO" || payment.estado === "ERROR") {
          paymentRetryLink.hidden = true;
          paymentReturnStatus.textContent =
            "El pago no fue aprobado. Puedes volver a intentar la contratación.";
          return;
        }
        if (payment.estado === "EXPIRADO") {
          paymentRetryLink.hidden = true;
          paymentReturnStatus.textContent =
            "El plazo para pagar venció. Vuelve a la cotización para iniciar un nuevo intento.";
          return;
        }
        if (payment.estado === "REQUIERE_REVISION") {
          paymentRetryLink.hidden = true;
          paymentReturnStatus.textContent =
            "Recibimos el pago, pero necesitamos revisar la reserva. Contáctanos antes de volver a pagar.";
          return;
        }
        paymentRetryLink.hidden = !payment.init_point;
        if (payment.init_point) paymentRetryLink.href = payment.init_point;
        paymentReturnStatus.textContent =
          "El pago todavía está pendiente. Puedes reintentar en Mercado Pago; la reserva aún no está confirmada.";
      } catch (error) {
        paymentReturnStatus.textContent = error.message;
      }
      await new Promise((resolve) => window.setTimeout(resolve, 2000));
    }
    paymentReturnStatus.textContent =
      "Aún no recibimos la confirmación del pago. No vuelvas a pagar; revisa esta página más tarde o contáctanos.";
  };

  // Inicialización
  populateEventTimes();
  updateMinimumEventDate();
  eventDateInput.addEventListener("focus", updateMinimumEventDate);
  eventDateInput.addEventListener("change", checkScheduleAvailability);
  eventTimeInput.addEventListener("change", checkScheduleAvailability);
  durationSelect.addEventListener("change", checkScheduleAvailability);
  calculateQuote();
  checkBackendHealth();
  synchronizeAdminSession();
  checkReturnedPayment();
});
