
document.addEventListener("DOMContentLoaded", function() {
    var scheduleTypeSelect = document.querySelector('#scheduleType');
    var scheduleOnInput = document.querySelector('#scheduleOnInput');
    
    scheduleTypeSelect.addEventListener('change', function()

     {
        
        var selectedScheduleType = scheduleTypeSelect.value;
        if (selectedScheduleType === 'Daily') {
            scheduleOnInput.innerHTML = '<input class="form-control" id="" name="scheduleOn" type="text" value="" disabled></input>';
        } else if (selectedScheduleType === 'Weekly') {
            scheduleOnInput.innerHTML = '<select class="form-control" name="scheduleOn", required>' +
                '<option value="Sunday">Sunday</option>' +
                '<option value="Monday">Monday</option>' +
                '<option value="Tuesday">Tuesday</option>' +
                '<option value="Wednesday">Wednesday</option>' +
                '<option value="Thursday">Thursday</option>' +
                '<option value="Friday">Friday</option>' +
                '<option value="Saturday">Saturday</option>' +
                '</select>';
        } else if (selectedScheduleType === 'Monthly') {
            scheduleOnInput.innerHTML = '<input class="form-control" type="number" name="scheduleOn" min="1" max="31", placeholder="Enter day no. 1 to 31"required>';
        } else if (selectedScheduleType === 'Yearly' || selectedScheduleType === 'Once') {
            scheduleOnInput.innerHTML = '<input type="date" class="form-control" name="scheduleOn" min="{{ (now() + timedelta(days=1)).strftime(\'%Y-%m-%d\') }}", required>';
        } else {
            scheduleOnInput.innerHTML = '<input class="form-control" id="" name="scheduleOn" type="text" value="", required>';
        }
    });
});
