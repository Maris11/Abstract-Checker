$(document).ready(function() {
    const average = array => array.reduce((a, b) => parseFloat(a) + parseFloat(b)) / array.length;

    $('#check-btn').click(function() {
        var myString = $('#input-abstract').val();
        $.ajax({
            url: 'http:/127.0.0.1:8000',
            method: 'POST',
            data: myString,
            success: function(response) {
                response = JSON.parse(response)
                removeElementsWithClass('sentence')

                for(let i = 0; i < response[0].length; i++) {
                    addSentence(i + 1, response[0][i], response[1][i])
                }
                console.log(response[1])
                $('#average-percentage').text(average(response[1]).toFixed(1))
            },
            error: function(xhr, status, error) {
                $('#percentage').textContent = error
            }
        });
    });

    function removeElementsWithClass(name) {
        var elements = document.getElementsByClassName(name);

        while (elements.length > 0) {
          elements[0].remove();
        }
    }

    function addSentence(index, sentence, percentage) {
        // Create a new row element with the Bootstrap class
        var row = $('<div class="row pt-2 sentence"></div>');

        // Create the first column with the index
        var indexCol = $('<div class="col-md-1 text-center">' + index + '</div>');

        // Create the second column with the sentence
        var sentenceCol = $('<div class="col-md-11" title="' + percentage + '%">' + sentence + '</div>');
        sentenceCol.css('color', getColorScale(percentage))

        // Add both columns to the row
        row.append(indexCol);
        row.append(sentenceCol);

        $('#sentences').append(row)
    }

    function getColorScale(percent) {
        // Set the minimum and maximum percentages for the scale
        var minPercent = 0;
        var maxPercent = 100;

        // Calculate the color based on the percentage
        var red = Math.round(255 * (percent - minPercent) / (maxPercent - minPercent));
        var green = Math.round(255 * (maxPercent - percent) / (maxPercent - minPercent));
        var blue = 0;

        // Return the color as a CSS string
        return 'rgb(' + red + ', ' + green + ', ' + blue + ')';
    }

    var container = $('#color-scale')
    var width = container.width()

    function createColorScale() {
        for (var i = 0; i <= 100; i++) {
            var color = getColorScale(i);
            var el = $('<div class="scale-color">').css('background-color', color).css('width', container.width()/101);
            container.append(el);
        }
    }

    createColorScale()

    $(window).on('resize', function() {
        if(container.width() !== width) {
            width = container.width()
            removeElementsWithClass('scale-color')
            createColorScale()
        }
    });
});