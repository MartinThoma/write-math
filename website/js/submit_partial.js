function submitPartial(raw_data_id, latex, strokes, successHandler) {
    $.ajax({
      type: "POST",
      url: "../api/submit-partial-answer.php",
      data: {'latex_partial': latex, 'strokes': strokes, 'raw_data_id': raw_data_id},
      success: function(data)
        {
            console.log(data);
            successHandler();
        },
      dataType: "json",
      error: function(xhr, status, error) {
            console.log("Error while sending the unaccept:");
            console.log(status);
            console.log(error);
      }
    });
}