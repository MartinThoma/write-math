function unacceptPartialAnswer(raw_data_id, formula_id, successHandler) {
    $.ajax({
      type: "POST",
      url: "../api/set-unaccept-partial.php",
      data: {'partial_answer_id': formula_id},
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