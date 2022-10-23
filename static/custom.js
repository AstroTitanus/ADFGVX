$(() => {

    // ALPHABET CONSTRUCTION
    const ALPHABET = Array.from(Array(26)).map((e, i) => i + 65).map((x) => String.fromCharCode(x));
    const NUMBERS = Array.from(Array(10)).map((e, i) => i + 48).map((x) => String.fromCharCode(x));

    // ALPHABETS CONSTANTS
    const ALPHABET_SK = ALPHABET.filter(letter => letter != "V");
    const ALPHABET_CZ = ALPHABET.filter(letter => letter != "Q");
    const ALPHABET_LONG = ALPHABET.concat(NUMBERS);

    // TODO: UPDATE THIS
    let CURR_ALPHABET = undefined;


    function getLanguage() {
        let lang = $("#lang").text();
        if (lang) return lang;
        return undefined;
    }


    function getMode() {
        let mode = $("#matrix-label").val();
        return mode;
    }


    function getUnusedLetters(tableId) {
        let unusedLetters = CURR_ALPHABET;
        let tableAlphabet = getTableData(tableId);
        tableAlphabet.forEach(row => {
            row.forEach(letter => {
                unusedLetters = unusedLetters.filter(alph_letter => alph_letter != letter);
            });
        });
        return unusedLetters
    }


    function updateUnusedPrint(unused) {
        let unusedOut = unused.length != 0 ? unused.join(", ") : "✅ All alphabet characters are used.";
        $("#unused-letters").text(unusedOut);
    }


    function getTableData(tableId) {
        var myTableArray = [];

        $(`table#${tableId} tr`).each(function() {
            var arrayOfThisRow = [];
            var tableData = $(this).find('td');
            if (tableData.length > 0) {
                tableData.each(function() { arrayOfThisRow.push($(this).text().toUpperCase()); });
                myTableArray.push(arrayOfThisRow);
            }
        });

        return myTableArray;
    }


    function setTableListeners(tableId, alphabet) {
        $(`table#${tableId} tr`).each(function() {
            var tableData = $(this).find('td');
            if (tableData.length > 0) {
                tableData.each(function() {
                    $(this).on("input", function(e) {

                        // Setup
                        let text = $(this).text();
                        let inputLetter = e.originalEvent.data;
                        inputLetter = inputLetter == undefined ? undefined : inputLetter.toUpperCase();

                        // Dont allow input except for valid alphabet characters
                        if (alphabet.includes(inputLetter)) {
                            $(this).text(inputLetter);
                        } else {
                            $(this).text("-");
                        }

                        // Refresh unused characters
                        let unused = getUnusedLetters(tableId);
                        updateUnusedPrint(unused);

                    });
                });
            }
        });

    }

    function setDecryptWithAlphabet(mode) {
        let el = $('#decrypt-with-alphabet');
        let tableDataStr = JSON.stringify(getTableData('alphabet-matrix'));
        let langParam = '';
        if (mode == "ADFGX") {
            if (getLanguage() == 'SK') langParam = 'lang=SK&';
            else if (getLanguage() == 'CZ') langParam = 'lang=CZ&';
        }
        el.attr("href", `/decrypt?mode=${mode}&${langParam}alphabet=${tableDataStr}`);
    }

    // Default alphabet
    CURR_ALPHABET = ALPHABET_LONG;

    // Set alphabet according to mode
    let mode = getMode();
    if (mode == "ADFGX") {
        if (getLanguage() == 'SK') CURR_ALPHABET = ALPHABET_SK;
        else if (getLanguage() == 'CZ') CURR_ALPHABET = ALPHABET_CZ;
    }

    // Set input listeners to all td
    setTableListeners("alphabet-matrix", CURR_ALPHABET);

    // Print initial unused characters
    let unused = getUnusedLetters("alphabet-matrix");
    updateUnusedPrint(unused);

    // Set href on decrypt with alphabet links
    setDecryptWithAlphabet(mode);

    $('#form').submit((e) => {
        let alphabetMatrixObj = { data: getTableData("alphabet-matrix") };
        let alphabetMatrixJsonStr = JSON.stringify(alphabetMatrixObj);

        let customInput = $("<input>", { type: "hidden", name: "alphabet_matrix", value: alphabetMatrixJsonStr });
        $('#form').append(customInput);
    });

});