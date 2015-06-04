function acceptPartialAnswer(raw_data_id, answer_id, successHandler) {
    $.ajax({
      type: "POST",
      url: "../api/set-accept-partial.php",
      data: {'raw_data_id': raw_data_id, 'answer_id': answer_id},
      success: function(data)
        {
            console.log(data);
            if (typeof(data.error) !== "undefined") {
                console.log(data.error);
            } else {
                successHandler();
            }
        },
      dataType: "json",
      error: function(xhr, status, error) {
            console.log("Error while sending the accept:");
            console.log(status);
            console.log(error);
      }
    });
}