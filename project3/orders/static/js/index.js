function qtyAdd(el) {
    qty = document.querySelector("#" + el)
    if (qty.value == 10) {
        alert("Max quantity is 10")
    }
    if (qty.value > 9) {
        return;
    }

    qty.value = ++qty.value
}

function qtySub(el) {
    qty = document.querySelector("#" + el)
    if (qty.value == 1) {
        alert("Minimum quantity is 1")
    }
    if (qty.value < 2) {
        return;
    }
    qty.value = --qty.value
}