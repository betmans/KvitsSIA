document.addEventListener('DOMContentLoaded', function() {
    const consentBanner = document.getElementById('cookieConsentBanner');
    const acceptButton = document.getElementById('acceptCookies');
    const declineButton = document.getElementById('declineCookies');

    console.log("CookieConsent.js script loaded and DOMContentLoaded."); // LOG A

    const storedConsent = localStorage.getItem('cookieConsent');
    console.log("LOG B: Value of 'cookieConsent' from localStorage on page load:", storedConsent);
    console.log("LOG C: Type of storedConsent:", typeof storedConsent);

    if (consentBanner) { // Ensure banner element exists before trying to modify it
        if (!storedConsent || storedConsent === "null" || storedConsent === "undefined") { // More robust check
            console.log("LOG D: No valid consent found in localStorage OR value is 'null'/'undefined' string. Showing banner.");
            consentBanner.style.display = 'flex'; // Assuming your CSS uses flex for display
        } else {
            console.log("LOG E: Valid consent ('" + storedConsent + "') FOUND in localStorage. Banner should remain hidden by CSS or explicitly hidden now.");
            consentBanner.style.display = 'none'; // Explicitly hide if found, to be safe
        }
    } else {
        console.error("LOG F: Cookie consent banner element (#cookieConsentBanner) not found!");
    }


    if (acceptButton) {
        acceptButton.addEventListener('click', function() {
            localStorage.setItem('cookieConsent', 'accepted');
            if (consentBanner) {
                consentBanner.style.display = 'none';
            }
            console.log("Cookie consent: 'accepted' SET in localStorage.");
        });
    } else {
        console.error("LOG G: Accept button (#acceptCookies) not found!");
    }

    if (declineButton) {
        declineButton.addEventListener('click', function() {
            localStorage.setItem('cookieConsent', 'declined');
            if (consentBanner) {
                consentBanner.style.display = 'none';
            }
            console.log("Cookie consent: 'declined' SET in localStorage.");
        });
    } else {
        console.error("LOG H: Decline button (#declineCookies) not found!");
    }
});