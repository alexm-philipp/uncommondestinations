document.addEventListener('DOMContentLoaded', ()=>{

    document.getElementById('location-input').addEventListener('input', function(){
        searchLocations();
        validate();
    });
    document.getElementById('budget').addEventListener('input', validate);
    document.getElementById('start_date').addEventListener('input', validate);
    document.getElementById('end_date').addEventListener('input', validate);
    document.getElementById('submit_form').addEventListener('click', checkFlight);

});

var inList = false;

function searchLocations(){
    var datalist = document.getElementById('departure-options');
    datalist.innerHTML = "";
    var input = document.getElementById('location-input').value;

    var url = `https://api.tequila.kiwi.com/locations/query?term=${input}&location_types=airport&limit=4`;
    var headers = {
        "Accept": "application/json",
        "apikey": "gGgmMRbcNFUZRWqo9Akg8HKtKgT5hmUJ"
      };

    fetch(url,{headers:headers})
    .then(response => response.json())
    .then(data => {
        console.log(data)
        //populate
        for (let i = 0; i < data.locations.length; i++){
            var option = document.createElement('option');
            option.value = data.locations[i].code;
            option.innerHTML = data.locations[i].name;
            datalist.appendChild(option);
        }
        //no submit without flight code
        inList = data.locations.some(location => location.code === input);
    })
    .catch(error => console.log(error));
}

function budget(){
    var budget = document.getElementById('budget').value;
        if (budget < 200){
            return false;
        }
        else if (budget >= 200){
            return true;
        }
}

function date_check(){

    var start_date_input = document.getElementById('start_date').value;
    var end_date_input = document.getElementById('end_date').value;

    c_d_before_format = dayjs();
    f_d_before_format = c_d_before_format.add(44, 'days');

    var current_date = c_d_before_format.format('YYYY-MM-DD')
    var maxFutureDate = f_d_before_format.format('YYYY-MM-DD')
    var start_date = start_date_input;
    var end_date = end_date_input;

    if (start_date === " " || end_date_input === " " || start_date > end_date || start_date < current_date || start_date > maxFutureDate || end_date > maxFutureDate){
        return false;
    }
    else {
        return true;
    }
}

function validate(){
    var submit_form = document.getElementById('submit_form');

    if (inList && budget() && date_check()){
        submit_form.disabled = false;
        return true;
    }
    else {
        submit_form.disabled = true;
        return false;
    }

}