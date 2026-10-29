(() => {
  const form = document.querySelector("#lead-form");
  const modal = document.querySelector("#lead-modal");
  const modalClose = document.querySelector("#close-lead-modal");
  const modalTrigger = document.querySelector("#open-lead-modal");
  const modalSessionKey = "etf-comparison-modal";
  const eventUrl = "/api/events";
  const campaignAttribution = readCampaignAttribution();
  const trackedOnce = new Set();
  let lastFocusTarget = null;
  let isUnlocked = false;
  let modalTimer;

  function readCampaignAttribution() {
    const query = new URLSearchParams(window.location.search);
    const values = {};
    for (const key of ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"]) {
      const raw = query.get(key);
      if (!raw) continue;
      const value = raw.trim().replace(/\s+/g, " ");
      if (value.length <= 100 && !value.includes("@") && !/https?:\/\//i.test(value)) values[key] = value;
    }
    return values;
  }

  function track(event, placement = "lead_flow") {
    const payload = JSON.stringify({ event, placement, ...campaignAttribution });
    if (navigator.sendBeacon) {
      navigator.sendBeacon(eventUrl, new Blob([payload], { type: "application/json" }));
      return;
    }
    fetch(eventUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: payload,
      keepalive: true,
    }).catch(() => {});
  }

  track("landing_page_view", "landing_page");

  function trackOnce(event, placement) {
    if (trackedOnce.has(event)) return;
    trackedOnce.add(event);
    track(event, placement);
  }

  const offerSection = document.querySelector("#lead-offer");
  if (offerSection && "IntersectionObserver" in window) {
    const offerObserver = new IntersectionObserver((entries) => {
      if (entries.some((entry) => entry.isIntersecting && entry.intersectionRatio >= 0.2)) {
        trackOnce("lead_offer_view", "lead_offer");
        offerObserver.disconnect();
      }
    }, { threshold: [0.2] });
    offerObserver.observe(offerSection);
  }

  function readModalState() {
    try { return sessionStorage.getItem(modalSessionKey); }
    catch (_error) { return "unavailable"; }
  }

  function writeModalState(value) {
    try { sessionStorage.setItem(modalSessionKey, value); }
    catch (_error) { /* modal remains usable if session storage is unavailable */ }
  }

  function openModal(invoker = document.activeElement) {
    if (!modal || modal.open) return;
    lastFocusTarget = invoker instanceof HTMLElement ? invoker : modalTrigger;
    modal.showModal();
    trackOnce("lead_offer_view", "lead_modal");
    document.querySelector("#first-name")?.focus({ preventScroll: true });
  }

  function closeModal() {
    if (modal?.open) modal.close("dismissed");
  }

  if (modal && readModalState() === null) {
    modalTimer = window.setTimeout(() => {
      if (readModalState() === null && !isUnlocked) openModal(document.activeElement);
    }, 6000);
  }

  modal?.addEventListener("close", () => {
    if (!isUnlocked) writeModalState("dismissed");
    if (lastFocusTarget?.isConnected) lastFocusTarget.focus({ preventScroll: true });
  });
  modalClose?.addEventListener("click", closeModal);
  modalTrigger?.addEventListener("click", () => openModal(modalTrigger));

  const comparison = document.querySelector("#comparison-table-wrap");
  if (comparison) {
    const recordComparisonInteraction = (event) => {
      if (!event.isTrusted || (event.target instanceof Element && event.target.closest("#lead-offer"))) return;
      trackOnce("comparison_interaction", "comparison");
      comparison.removeEventListener("pointerdown", recordComparisonInteraction);
      comparison.removeEventListener("keydown", recordComparisonInteraction);
      comparison.removeEventListener("scroll", recordComparisonInteraction);
    };
    comparison.addEventListener("pointerdown", recordComparisonInteraction, { passive: true });
    comparison.addEventListener("keydown", recordComparisonInteraction);
    comparison.addEventListener("scroll", recordComparisonInteraction, { passive: true });
  }

  document.querySelectorAll("[data-funnel-cta]").forEach((cta) => {
    cta.addEventListener("click", () => track("cta_interaction", cta.dataset.funnelCta));
  });

  if (!form) return;

  const submitButton = form.querySelector(".form-submit");
  const formStatus = document.querySelector("#form-status");
  const fullComparison = document.querySelector("#full-comparison");
  const unlockSuccess = document.querySelector("#unlock-success");
  const visitorName = document.querySelector("#visitor-name");
  const emailResult = document.querySelector("#email-result");
  const firstName = document.querySelector("#first-name");
  const email = document.querySelector("#email");
  const tableWrap = document.querySelector("#comparison-table-wrap");
  const formStartTargets = "#first-name, #email, #marketing-consent";
  const recordFormStart = (event) => {
    if (!event.isTrusted || !event.target.matches?.(formStartTargets)) return;
    trackOnce("form_start", "form");
    form.removeEventListener("pointerdown", recordFormStart);
    form.removeEventListener("input", recordFormStart);
    form.removeEventListener("change", recordFormStart);
    form.removeEventListener("keydown", recordFormStart);
  };
  form.addEventListener("pointerdown", recordFormStart, { passive: true });
  form.addEventListener("input", recordFormStart);
  form.addEventListener("change", recordFormStart);
  form.addEventListener("keydown", recordFormStart);

  function clearErrors() {
    document.querySelectorAll(".field-error").forEach((node) => { node.textContent = ""; });
    document.querySelectorAll(".field-group input").forEach((node) => node.removeAttribute("aria-invalid"));
  }

  function showValidationErrors(details) {
    const messages = {
      first_name: "Zadejte prosím své jméno.",
      email: "Zadejte prosím platnou e-mailovou adresu.",
    };
    let shown = false;
    for (const issue of details || []) {
      const field = issue.loc?.at(-1);
      const message = messages[field];
      const input = field === "first_name" ? firstName : field === "email" ? email : null;
      const error = field === "first_name"
        ? document.querySelector("#first-name-error")
        : field === "email" ? document.querySelector("#email-error") : null;
      if (input && error && message) {
        input.setAttribute("aria-invalid", "true");
        error.textContent = message;
        if (!shown) input.focus();
        shown = true;
      }
    }
    if (!shown) formStatus.textContent = "Zkontrolujte prosím jméno a e-mailovou adresu.";
  }

  async function requestConfirmation(emailAddress) {
    emailResult.textContent = "Srovnání je odemčeno. Zkoušíme odeslat potvrzovací e-mail…";
    try {
      const response = await fetch("/api/confirmation-email", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ email: emailAddress }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error("send_failed");

      if (result.email_status === "accepted") {
        emailResult.textContent = "Potvrzovací e-mail jsme předali k odeslání. Doručení do schránky nemůžeme zaručit.";
        track("email_accepted", "lead_flow");
      } else if (result.email_status === "not_configured") {
        emailResult.textContent = "Srovnání je odemčeno. Potvrzovací e-mail není nakonfigurován, proto nebyl odeslán.";
        emailResult.classList.add("is-error");
        track("email_not_configured", "lead_flow");
      } else {
        emailResult.textContent = "Srovnání je odemčeno. Potvrzovací e-mail se nepodařilo odeslat. Stránku si můžete uložit; později zadejte stejný e-mail a srovnání znovu otevřete.";
        emailResult.classList.add("is-error");
        track("email_failed", "lead_flow");
      }
    } catch (_error) {
      emailResult.textContent = "Srovnání je odemčeno. Nepodařilo se ověřit, zda byl potvrzovací e-mail odeslán. Stránku si můžete uložit; později zadejte stejný e-mail a srovnání znovu otevřete.";
      emailResult.classList.add("is-error");
      track("email_status_unknown", "lead_flow");
    }
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearErrors();
    formStatus.classList.remove("is-success");
    formStatus.textContent = "";
    emailResult.textContent = "";
    emailResult.classList.remove("is-error");
    const payload = {
      first_name: firstName.value,
      email: email.value,
      marketing_consent: form.elements.marketing_consent.checked,
      ...campaignAttribution,
    };

    submitButton.disabled = true;
    submitButton.classList.add("is-loading");
    submitButton.querySelector(".button-label").textContent = "Ukládáme žádost…";
    formStatus.textContent = "Ukládáme vaše údaje. Srovnání se otevře po potvrzení uložení.";

    try {
      const response = await fetch(form.action, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(payload),
      });
      const result = await response.json();

      if (response.status === 422) {
        formStatus.textContent = "";
        showValidationErrors(result.detail);
        return;
      }
      if (!response.ok || result.recorded !== true) {
        formStatus.textContent = result.detail || "Údaje se nepodařilo uložit. Zkuste to prosím znovu.";
        return;
      }

      tableWrap?.classList.add("is-unlocked");
      const lockCallout = tableWrap?.querySelector(".lock-callout");
      if (lockCallout) lockCallout.hidden = true;
      document.querySelectorAll("[data-locked]").forEach((group) => {
        group.removeAttribute("data-locked");
        group.removeAttribute("aria-hidden");
      });
      fullComparison.hidden = false;
      fullComparison.setAttribute("aria-hidden", "false");
      visitorName.textContent = payload.first_name.trim().replace(/\s+/g, " ");
      formStatus.textContent = "Vaše žádost byla zaznamenána.";
      formStatus.classList.add("is-success");
      isUnlocked = true;
      writeModalState("unlocked");
      if (modalTimer) window.clearTimeout(modalTimer);
      closeModal();

      requestConfirmation(payload.email);

      const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      fullComparison.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
      unlockSuccess.focus({ preventScroll: true });
    } catch (_error) {
      formStatus.textContent = "Nepodařilo se spojit se serverem. Zkontrolujte připojení a zkuste to znovu.";
    } finally {
      submitButton.disabled = false;
      submitButton.classList.remove("is-loading");
      submitButton.querySelector(".button-label").textContent = "Odemknout úplné srovnání";
    }
  });
})();
