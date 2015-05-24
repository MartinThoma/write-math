function acceptPartialAnswer(raw_data_id, formula_id, successHandler) {
    $.ajax({
      type: "POST",
      url: "../api/set-accept-partial.php",
      data: {'raw_data_id': raw_data_id, 'partial_answer_id': formula_id},
      success: function(data)
        {
            console.log(data);
            if (typeof(data.error) == undefined) {
                successHandler();
            } else {
                
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