function annuityValue() {
    // Get input values
    const annuityValueForm = document.querySelector("#annuity-value");
    const values = annuityValueForm.querySelectorAll(".form-control");
    const radioValues = annuityValueForm.querySelectorAll(".form-check-input");
    // Save input values
    const startAmt = values[0].value;
    const duration = values[1].value;
    const interest = values[2].value / 100;
    const compounding = values[3].value.toLowerCase();
    const contribution = values[4].value;
    // Save radio input values
    var contributionFreq;
    var annuityType;
    if (radioValues[0].checked) {
        contributionFreq = radioValues[0].value;
    } else {
        contributionFreq = radioValues[1].value;
    };
    if (radioValues[2].checked) {
        var annuityType = radioValues[2].value;
    } else {
        var annuityType = radioValues[3].value;
    };
    // Calculate answer
    answer = annuityValueAnswer(startAmt, duration, interest, compounding, contribution, contributionFreq, annuityType);
    // Display answer
    document.querySelector("#annuity-value-answer").innerHTML = `Answer: ${answer}`;
}

// Calculate the value of the annuity
function annuityValueAnswer(startAmt, duration, interest, compounding, contribution, contributionFreq, annuityType) {
    // Corner cases
    if (interest == 0) {
        if (contributionFreq == "monthly") {
            return Number(startAmt) + Number(contribution) * duration * 12;
        } else {
            return Number(startAmt) + Number(contribution) * duration;
        };
    };
    if (duration < 0) {
        return "Duration must be positive";
    }
    // Normal calculations
    var rate = interestRate(interest, compounding, contributionFreq);
    if (contributionFreq == "monthly") {
        var cum = ((1 + rate / 12) ** (duration * 12) - 1) / (rate / 12);
        var startVal = startAmt * ((1 + rate / 12) ** (duration*12));
        if (annuityType == "ordinary") {
            return (startVal + contribution * cum).toFixed(2);
        } else {
            return (startVal + (contribution * cum) * (1 + rate)).toFixed(2);
        };
    } else {
        var cum = ((1 + rate) ** duration - 1) / rate;
        var startVal = startAmt * (1 + rate) ** duration;
        if (annuityType == "ordinary") {
            return (startVal + contribution * cum).toFixed(2);
        } else {
            return (startVal + (contribution * cum) * (1 + rate)).toFixed(2);
        };
    };
}


function interestConversion() {
    // Get input values
    const interestConversionForm = document.querySelector("#interest-conversion");
    const values = interestConversionForm.querySelectorAll(".form-control");
    // Save input values
    const interest = values[0].value / 100;
    const inputCompounding = values[1].value.toLowerCase();
    const outputCompounding = values[2].value.toLowerCase();
    // Calculate answer
    annualInterest = interestRate(interest, inputCompounding, outputCompounding);
    answer = (annualInterest * 100).toFixed(5)
    // Display answer
    document.querySelector("#interest-conversion-answer").innerHTML = `Answer: ${answer}%`;
}


// Calculate rate corresponding to input and output compounding type
function interestRate(rate, inputPeriod, outputPeriod) {
    if (rate == 0) { 
        return 0;
    }
    const amounts = {
        "annually": 1,
        "semiannually": 2,
        "quarterly": 4,
        "monthly": 12,
        "weekly": 52,
        "daily": 365,
    };
    
    if (inputPeriod == outputPeriod) {
        return rate;
    } else if (inputPeriod == "continuously" || outputPeriod == "continuously") {
        if (inputPeriod == "continuously") {
            var annual = Math.E ** rate;
            return (annual**(1 / amounts[outputPeriod]) - 1) * amounts[outputPeriod];
        } else {
            var annual = (1 + rate / amounts[inputPeriod])**amounts[inputPeriod];
            console.log(annual);
            return Math.log(annual);
        }
    } else if (!inputPeriod in amounts || !outputPeriod in amounts) {
        return rate;
    } else {
        var annual = (1 + rate / amounts[inputPeriod])**amounts[inputPeriod];
        return (annual**(1 / amounts[outputPeriod]) - 1) * amounts[outputPeriod];
    };
}