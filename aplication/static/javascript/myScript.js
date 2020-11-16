var baseUrl = document.getElementById("myiframe").src;

$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });
});

function change_page(pageName) {
    var newUrl = baseUrl + "&pageName=" + pageName;
    var report = document.getElementById("myiframe");
    report.src = newUrl;
}





function service() {


    var edad_ = parseInt(document.getElementById('age').value);
    var estrato = parseInt(document.getElementById('stratum').value);
    var ocupacion_ = parseInt(document.getElementById('ocupation').value);
    var sexo_ = document.getElementsByName('gender')[0].checked;
    var comor = [];
    var trab_salud = document.getElementById('trabsalud').checked;
    var tos = document.getElementById('tos').checked;
    var fiebre = document.getElementById('fiebre').checked;
    var odinofagia = document.getElementById('odinofagia').checked;
    var dif_res = document.getElementById('dif_res').checked;
    var adinamia = document.getElementById('adinamia').checked;
    var asma = document.getElementById('asma').checked;
    var epoc = document.getElementById('epoc').checked;
    var diabetes = document.getElementById('diabetes').checked;
    var vih = document.getElementById('vih').checked;
    var enf_card = document.getElementById('enf_card').checked;
    var cancer = document.getElementById('cancer').checked;
    var desnutricion = document.getElementById('desnutricion').checked;
    var obesidad = document.getElementById('obesidad').checked;
    var ins_renal = document.getElementById('ins_renal').checked;
    var otr_medinm = document.getElementById('otr_medinm').checked;
    var fumador = 2;//document.getElementById('fumador').checked;
    var tuberculos = document.getElementById('tuberculosis').checked;
    var hallaz_rad = document.getElementById('hallaz_rad').checked;
    var der_ple = document.getElementById('der_ple').checked;
    var der_per = document.getElementById('der_per').checked;
    var miocarditi = document.getElementById('miocarditi').checked;
    var septicemia = document.getElementById('septicemia').checked;
    var falla_resp = document.getElementById('falla_resp').checked;
    var rinorrea = document.getElementById('rinorrea').checked;
    var conjuntivi = document.getElementById('conjuntivi').checked;
    var cefalea = document.getElementById('cefalea').checked;
    var diarrea = document.getElementById('diarrea').checked;


    if (sexo_ == true) {
        sexo_ = 'M';
    }
    else {
        sexo_ = 'F';
    }


    if (trab_salud == true) { trab_salud = 1; }
    else { trab_salud = 2; }

    if (tos == true) { tos = 1; }
    else { tos = 2; }

    if (fiebre == true) { fiebre = 1; }
    else { fiebre = 2; }

    if (odinofagia == true) { odinofagia = 1; }
    else { odinofagia = 2; }

    if (dif_res == true) { dif_res = 1; }
    else { dif_res = 2; }

    if (adinamia == true) { adinamia = 1; }
    else { adinamia = 2; }

    if (asma == true) { asma = 1; }
    else { asma = 2; }

    if (epoc == true) { epoc = 1; }
    else { epoc = 2; }

    if (diabetes == true) { diabetes = 1; }
    else { diabetes = 2; }

    if (vih == true) { vih = 1; }
    else { vih = 2; }

    if (enf_card == true) { enf_card = 1; }
    else { enf_card = 2; }

    if (cancer == true) { cancer = 1; }
    else { cancer = 2; }

    if (desnutricion == true) { desnutricion = 1; }
    else { desnutricion = 2; }

    if (obesidad == true) { obesidad = 1; }
    else { obesidad = 2; }

    if (ins_renal == true) { ins_renal = 1; }
    else { ins_renal = 2; }

    if (otr_medinm == true) { otr_medinm = 1; }
    else { otr_medinm = 2; }

    /*if (fumador == true) { fumador = 1; }
    else { fumador = 2; }*/

    if (tuberculos == true) { tuberculos = 1; }
    else { tuberculos = 2; }

    if (hallaz_rad == true) { hallaz_rad = 1; }
    else { hallaz_rad = 2; }

    if (der_ple == true) { der_ple = 1; }
    else { der_ple = 2; }

    if (der_per == true) { der_per = 1; }
    else { der_per = 2; }

    if (miocarditi == true) { miocarditi = 1; }
    else { miocarditi = 2; }

    if (septicemia == true) { septicemia = 1; }
    else { septicemia = 2; }

    if (falla_resp == true) { falla_resp = 1; }
    else { falla_resp = 2; }

    if (rinorrea == true) { rinorrea = 1; }
    else { rinorrea = 2; }

    if (conjuntivi == true) { conjuntivi = 1; }
    else { conjuntivi = 2; }

    if (cefalea == true) { cefalea = 1; }
    else { cefalea = 2; }

    if (diarrea == true) { diarrea = 1; }
    else { diarrea = 2; }



    var jsonSend = JSON.stringify({
        'edad_': edad_,
        'estrato': estrato,
        'ocupacion_': ocupacion_,
        'sexo_': sexo_,
        'trab_salud': trab_salud,
        'tos': tos,
        'fiebre': fiebre,
        'odinofagia': odinofagia,
        'dif_res': dif_res,
        'adinamia': adinamia,
        'asma': asma,
        'epoc': epoc,
        'diabetes': diabetes,
        'vih': vih,
        'enf_card': enf_card,
        'cancer': cancer,
        'desnutricion': desnutricion,
        'obesidad': obesidad,
        'ins_renal': ins_renal,
        'otr_medinm': otr_medinm,
        'fumador': fumador,
        'tuberculos': tuberculos,
        'hallaz_rad': hallaz_rad,
        'der_ple': der_ple,
        'der_per': der_per,
        'miocarditi': miocarditi,
        'septicemia': septicemia,
        'falla_resp': falla_resp,
        'rinorrea': rinorrea,
        'conjuntivi': conjuntivi,
        'cefalea': cefalea,
        'diarrea': diarrea
    })

    console.log(jsonSend);

    fetch('http://127.0.0.1:5000/api/predict', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: jsonSend
    })
        .then((respuesta) => {
            return respuesta.json();
        }).then((respuesta) => {
            console.log('respuesta')
            var prediction = respuesta.message[0].prediction * 100;
            console.log(prediction);
            document.getElementById('riesgo').innerHTML = prediction.toFixed(4) + " %";
        })
}