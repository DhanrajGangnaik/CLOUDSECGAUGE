// Function to check for SQL injection patterns
function isSafeInput(input) {
    const sqlInjectionPatterns = [
        /['";#@&\\\/*+%-]/,                  // Common SQL special characters
        /\b(OR|AND|UNION|SELECT|INSERT|DELETE|UPDATE|HAVING|DROP|BENCHMARK|SLEEP|WAITFOR|RLIKE|CONVERT|CHAR|INTO|FROM|WHERE|GROUP BY|ORDER BY)\b/i,
        /--/,                                 // SQL comment syntax
        /\d+\s*=\s*\d+/,                      // Expressions like 1=1
        /[^\w\s]AND[^\w\s]/i,                 // Statements with AND (e.g., "admin' AND 1=1")
        /[^\w\s]OR[^\w\s]/i,                  // Statements with OR (e.g., "admin' OR '1'='1")
        /(\b)[\w]*((\b)SLEEP|BENCHMARK|WAITFOR)/i, // Time-based injections
        /(\b)[\w]*((\b)RLIKE|LIKE|CHAR|UNION|CONCAT)/i,
        /(UNION\s+SELECT)/i,                   // UNION-based injections
        /%00|--|;/,                           // Null byte, comments, or semi-colon
    ];

    return !sqlInjectionPatterns.some(pattern => pattern.test(input));
}

// Function to validate all form inputs
function validateForm(form) {
    for (let i = 0; i < form.elements.length; i++) {
        const element = form.elements[i];
        if (element.type === 'text' || element.type === 'password' || element.type === 'textarea') {
            const value = element.value.trim();

            // Check for empty input or invalid input
            if (value === "" || !isSafeInput(value)) {
                alert("Invalid input detected! Please avoid using special characters or SQL keywords.");
                element.focus();
                return false;
            }
        }
    }
    return true;
}

// Add event listeners to validate inputs in real-time
document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("form");
    forms.forEach((form) => {
        form.addEventListener("submit", function (event) {
            if (!validateForm(form)) {
                event.preventDefault();
            }
        });
    });

    // Prevent pasting into input fields to avoid injecting payloads
    const inputs = document.querySelectorAll("input[type='text'], input[type='password'], textarea");
    inputs.forEach(input => {
        input.addEventListener("paste", function (e) {
            e.preventDefault();
            alert("Pasting is disabled for security reasons.");
        });
    });
});
