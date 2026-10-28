(() => {
  const form = document.querySelector("#lead-form");
  if (!form) return;

  const submitButton = form.querySelector(".form-submit");
  const formStatus = document.querySelector("#form-status");
  const fullComparison = document.querySelector("#full-comparison");
  const unlockSuccess = document.querySelector("#unlock-success");
  const visitorName = document.querySelector("#visitor-name");
  const emailResult = document.querySelector("#email-result");
  const firstName = document.querySelector("#first-name");
  const email = document.querySelector("#email");

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
    if (!shown) {
      formStatus.textContent = "Zkontrolujte prosím jméno a e-mailovou adresu.";
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

      // Only a positive server confirmation of the database write unlocks content.
      fullComparison.hidden = false;
      fullComparison.setAttribute("aria-hidden", "false");
      visitorName.textContent = payload.first_name.trim().replace(/\s+/g, " ");
      formStatus.textContent = "Vaše žádost byla zaznamenána.";
      formStatus.classList.add("is-success");

      if (result.email_status === "accepted") {
        emailResult.textContent = "Potvrzovací e-mail jsme předali k odeslání. Doručení do schránky nemůžeme zaručit.";
      } else if (result.email_status === "not_configured") {
        emailResult.textContent = "Srovnání je odemčeno. Potvrzovací e-mail není nakonfigurován, proto nebyl odeslán.";
        emailResult.classList.add("is-error");
      } else {
        emailResult.textContent = "Srovnání je odemčeno. Potvrzovací e-mail se nepodařilo odeslat. Stránku si můžete uložit; později zadejte stejný e-mail a srovnání znovu otevřete.";
        emailResult.classList.add("is-error");
      }

      const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      fullComparison.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
      unlockSuccess.focus({ preventScroll: true });
    } catch (_error) {
      formStatus.textContent = "Nepodařilo se spojit se serverem. Zkontrolujte připojení a zkuste to znovu.";
    } finally {
      submitButton.disabled = false;
      submitButton.classList.remove("is-loading");
      submitButton.querySelector(".button-label").textContent = "Otevřít srovnání";
    }
  });
})();
