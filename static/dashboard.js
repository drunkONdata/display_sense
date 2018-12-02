let update_dashboards = function() {
    setInterval(get_foot_traffic_last_day, 2000)
    setInterval(get_head_turns_last_day, 2000)
    setInterval(get_general_sentiment_last_day, 2000)
    setInterval(get_analytics_last_day, 2000)
}

let draw_plotly = function() {
    var data = [{
        x: ['giraffes', 'orangutans', 'monkeys'],
        y: [20, 14, 23],
        type: 'scatter'
    }];

    Plotly.newPlot('foot_traffic_dashboard', data);
}

let get_analytics_last_day = function () {
    startTime = Date.now()
    startTime -= 24 * 3600 * 1000
    $.ajax({
        url: '/analytics?start=' + startTime,
        type: 'GET',
        success: function (data) {
            draw_dashboards(data);
        }
    });
};

function draw_dashboards(data) {
    let dict = JSON.parse(data);
    now = Date.now()

    foot_traffic = dict['foot_traffic']
    var foot_traffic_data = [{
        x: $.map(foot_traffic, function(value, key) { return now - parseInt(key) }),
        y: $.map(foot_traffic, function(value, key) { return value }),
        mode: 'lines',
        name: 'Foot traffic'
    }];

    var layout = {
        title: 'Foot traffic'
    };

    Plotly.newPlot('foot_traffic_dashboard', foot_traffic_data, layout);

    head_turns = dict['head_turns']
    var head_turns_data = [{
        x: $.map(head_turns, function(value, key) { return now - parseInt(key) }),
        y: $.map(head_turns, function(value, key) { return value }),
        mode: 'lines',
        name: 'Head turns'
    }];

    var layout = {
        title: 'Head turns'
    };

    Plotly.newPlot('head_turns_dashboard', head_turns_data, layout);

    male_head_turns = dict['male_head_turns']
    var male_head_turns_data = {
        x: $.map(male_head_turns, function(value, key) { return now - parseInt(key) }),
        y: $.map(male_head_turns, function(value, key) { return value }),
        fill: 'tozeroy',
        type: 'scatter',
        mode: 'none',
        name: 'Male'
    };

    female_head_turns = dict['female_head_turns']
    var female_head_turns_data = {
        x: $.map(female_head_turns, function(value, key) { return now - parseInt(key) }),
        y: $.map(female_head_turns, function(value, key) { return value }),
        fill: 'tonexty',
        type: 'scatter',
        mode: 'none',
        name: 'Female'
    };

    gender_head_turns_data = [male_head_turns_data, female_head_turns_data]

    var layout = {
        title: 'Head turns by gender'
    };

    Plotly.newPlot('gender_head_turns_dashboard', gender_head_turns_data, layout);

    youth_head_turns = dict['youth_head_turns']
    var youth_head_turns_data = {
        x: $.map(youth_head_turns, function(value, key) { return now - parseInt(key) }),
        y: $.map(youth_head_turns, function(value, key) { return value }),
        fill: 'tozeroy',
        type: 'scatter',
        mode: 'none',
        name: 'Youth'
    };

    adult_head_turns = dict['adult_head_turns']
    var adult_head_turns_data = {
        x: $.map(adult_head_turns, function(value, key) { return now - parseInt(key) }),
        y: $.map(adult_head_turns, function(value, key) { return value }),
        fill: 'tozeroy',
        type: 'scatter',
        mode: 'none',
        name: 'Adult'
    };

    seniors_head_turns = dict['seniors_head_turns']
    var seniors_head_turns_data = {
        x: $.map(seniors_head_turns, function(value, key) { return now - parseInt(key) }),
        y: $.map(seniors_head_turns, function(value, key) { return value }),
        fill: 'tozeroy',
        type: 'scatter',
        mode: 'none',
        name: 'Seniors'
    };

    age_head_turns_data = [youth_head_turns_data, adult_head_turns_data, seniors_head_turns_data]

    var layout = {
        title: 'Head turns by age'
    };

    Plotly.newPlot('age_head_turns_dashboard', age_head_turns_data, layout);

    happy_head_turns = dict['happy_head_turns']
    var happy_head_turns_data = {
        x: $.map(happy_head_turns, function(value, key) { return now - parseInt(key) }),
        y: $.map(happy_head_turns, function(value, key) { return value }),
        fill: 'tozeroy',
        type: 'scatter',
        mode: 'none',
        name: 'Happy'
    };

    calm_head_turns = dict['calm_head_turns']
    var calm_head_turns_data = {
        x: $.map(calm_head_turns, function(value, key) { return now - parseInt(key) }),
        y: $.map(calm_head_turns, function(value, key) { return value }),
        fill: 'tozeroy',
        type: 'scatter',
        mode: 'none',
        name: 'Calm'
    };

    surprised_head_turns = dict['surprised_head_turns']
    var surprised_head_turns_data = {
        x: $.map(surprised_head_turns, function(value, key) { return now - parseInt(key) }),
        y: $.map(surprised_head_turns, function(value, key) { return value }),
        fill: 'tozeroy',
        type: 'scatter',
        mode: 'none',
        name: 'Surprised'
    };

    disgusted_head_turns = dict['disgusted_head_turns']
    var disgusted_head_turns_data = {
        x: $.map(disgusted_head_turns, function(value, key) { return now - parseInt(key) }),
        y: $.map(disgusted_head_turns, function(value, key) { return value }),
        fill: 'tozeroy',
        type: 'scatter',
        mode: 'none',
        name: 'Disgusted'
    };

    sad_head_turns = dict['sad_head_turns']
    var sad_head_turns_data = {
        x: $.map(sad_head_turns, function(value, key) { return now - parseInt(key) }),
        y: $.map(sad_head_turns, function(value, key) { return value }),
        fill: 'tozeroy',
        type: 'scatter',
        mode: 'none',
        name: 'Sad'
    };

    angry_head_turns = dict['angry_head_turns']
    var angry_head_turns_data = {
        x: $.map(angry_head_turns, function(value, key) { return now - parseInt(key) }),
        y: $.map(angry_head_turns, function(value, key) { return value }),
        fill: 'tozeroy',
        type: 'scatter',
        mode: 'none',
        name: 'Angry'
    };

    confused_head_turns = dict['confused_head_turns']
    var confused_head_turns_data = {
        x: $.map(confused_head_turns, function(value, key) { return now - parseInt(key) }),
        y: $.map(confused_head_turns, function(value, key) { return value }),
        fill: 'tozeroy',
        type: 'scatter',
        mode: 'none',
        name: 'Confused'
    };

    emotion_head_turns_data = [happy_head_turns_data, calm_head_turns_data, disgusted_head_turns_data, surprised_head_turns_data, sad_head_turns_data, angry_head_turns_data, confused_head_turns_data]

    var layout = {
        title: 'Head turns by emotion'
    };

    Plotly.newPlot('emotion_head_turns_dashboard', emotion_head_turns_data, layout);
}

let get_foot_traffic_last_day = function () {
    $.ajax({
        url: '/foot_traffic_last_day',
        type: 'GET',
        success: function (data) {
            update_foot_traffic_last_day(data);
        }
    });
};

function update_foot_traffic_last_day(data) {
    html = `<p>Foot traffic</p>` + data
    $('#foot_traffic').html(html);
}

let get_head_turns_last_day = function () {
    $.ajax({
        url: '/head_turns_last_day',
        type: 'GET',
        success: function (data) {
            update_head_turns_last_day(data);
        }
    });
};

function update_head_turns_last_day(data) {
    html = `<p>Head turns</p>` + data
    $('#head_turns').html(html);
}

let get_general_sentiment_last_day = function () {
    $.ajax({
        url: '/general_sentiment_last_day',
        type: 'GET',
        success: function (data) {
            update_general_sentiment_last_day(data);
        }
    });
};

function update_general_sentiment_last_day(data) {
    html = `<p>General sentiment</p>` + data
    $('#general_sentiment').html(html);
}







let get_input_text = function () {
    let X = $("input#text_input").val()
    return { "text_input": X }
};

let send_text_json = function (X) {
    $.ajax({
        url: '/submit',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        success: function (data) {
            drawTable(data);
        },
        data: JSON.stringify(X) //This gets sent to the submit page.
    });
};

function drawTable(data) {
    var html = '';
    let array = JSON.parse(data);
    for (var i = 0; i < array.length; i++) {
        research_areas_html = ""
        array[i].research_areas.forEach(research_area => {
            research_areas_html += `<li>` + research_area + `</li>`
        });

        html += `
            <div class="col-lg-8 post-list">
                <div class="single-post d-flex flex-row">
                    <div class="thumb">
                        <img src="` + array[i].photo_link + `" alt="` + array[i].faculty_name + `" width="150" height="200">
                    </div>
                    <div class="details" style="padding-left: 20px">
                        <div class="title d-flex flex-row justify-content-between">
                            <div class="titles">
                                <a href="professor/` + array[i].id + `">
                                    <h3>` + array[i].faculty_name + `</h3>
                                </a>
                                <h5><b>` + array[i].university_name + `</b></h5>
                                <h6><b>Designation:</b> ` + array[i].title + `</h6>
                                <h6><b>Email:</b> ` + array[i].email + `</h6>
                                <h6><b>Phone:</b> ` + array[i].phone + `</h6>
                                <h6><b>Office:</b> ` + array[i].office + `</h6>
                                <h6><b>Website:</b> <a href="` + array[i].page + `">` + array[i].page + `</a></h6>
                            </div>
                        </div>
                    </div>
                </div>
			</div>`
    }

    $('#facecards-section').addClass("section-gap");
    $('#facecards').html(html);
    $('#facecards')[0].scrollIntoView(true, { behavior: 'smooth' });
    window.scrollBy(0, -70);
}

// button on-click function
let predict = function () {
    let X = get_input_text();
    send_text_json(X);
};

// select on-change function
let plot_topic_distribution = function (prof_id) {
    if (prof_id == "-1") {
        $('#plot').html('')
    }
    else {
        $.ajax({
            url: '/professor-topics/' + prof_id,
            contentType: "application/json; charset=utf-8",
            type: 'POST',
            success: function (response) {
                $('#plot').html(response)
            }
        });
    }

};
