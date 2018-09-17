var mChart;

function loadEcharts(mChart, name) {
    var template = 'id_echarts_container_' + name
    var url = '/boards/options/' + 'dash_' + name + '/';
    if (mChart != null) {
        mChart.clear();
    }
    mChart = echarts.init(document.getElementById(template));
    mChart.showLoading();
    $.ajax({
        url: url,
        type: "GET",
        data: null,
        dataType: "json"
    }).done(function(data) {
        mChart.hideLoading();
        mChart.setOption(data);
        console.log(data);
    });
}
$(document).ready(function() {
    $('a[data-echarts-name]').on('click', function() {
        var name = $(this).data('echartsName');
        switch (name) {
            case 'yield':
                loadEcharts(mChart, name);
            default:
                break;
        }
    });
    loadEcharts(mChart, 'yield');

    setInterval(function() { loadEcharts(mChart, 'yield'); }, 10000); /* update every 6 seconds*/
});