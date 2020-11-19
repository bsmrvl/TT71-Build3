var timer;

function valquery(){
    var goal = parseFloat(document.forms['queryform']['goal'].value);
    if(goal < 0 || goal > 10000000){
        flash('Goal must be between $0 and $10,000,000')
        return false;
    }
}

function valpred(){
    var form = document.forms['predform'];
    var goal = parseFloat(form['goal'].value);
    if(form['title'].value == '' || form['blurb'].value == '' || form['category'].value == '' || form['goal'].value == ''){
        flash('All fields are required');
        return false;
    }
    if(goal < 0 || goal > 10000000){
        flash('Goal must be between $0 and $10,000,000');
        return false;
    }
}

function flash(message){
    var alertbox = document.getElementById('alertbox')
    alertbox.innerHTML = message;
    alertbox.style.visibility = 'visible';
    clearTimeout(timer);
    timer = setTimeout(() => {
        alertbox.style.visibility = 'hidden';
    }, 1500);
}

function streamtab(stream){
    if(window.matchMedia("(max-width: 500px)").matches){
        var ftoggle = document.getElementById('ftoggle');
        var stoggle = document.getElementById('stoggle');
        var fstream = document.getElementById('fstream');
        var sstream = document.getElementById('sstream');
        if(stream == 0){
            ftoggle.style.backgroundColor = 'rgba(0,0,0, .07)';
            stoggle.style.backgroundColor = 'white';
            fstream.style.display = 'block';
            sstream.style.display = 'none';
        } else {
            stoggle.style.backgroundColor = 'rgba(0,0,0, .07)';
            ftoggle.style.backgroundColor = 'white';
            sstream.style.display = 'block';
            fstream.style.display = 'none';
        }
    }
}