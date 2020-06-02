(function() {
  var NOT_DISPLAY_REASON = '0'
  var DISPLAY_REASON = '1'

  document.querySelectorAll('.hide-reason').forEach(function(element) {
    element.classList.add('hide')
  })

  document.querySelectorAll('.show-reason > button').forEach(function(element) {
    element.addEventListener('click', function() {
      changeDisplayReason(element.closest('td'))
    })
  })
  document.querySelectorAll('.hide-reason > button').forEach(function(element) {
    element.addEventListener('click', function() {
      changeDisplayReason(element.closest('td'))
    })
  })

  function changeDisplayReason(element) {
    var currentStatus = element.querySelector('.display_status').value
    var updateStatus = currentStatus === NOT_DISPLAY_REASON ? DISPLAY_REASON : NOT_DISPLAY_REASON
    if (updateStatus === NOT_DISPLAY_REASON) {
      element.querySelector('.show-reason').classList.remove('hide')
      element.querySelector('.hide-reason').classList.add('hide')
      element.querySelector('.display_status').value = NOT_DISPLAY_REASON
      return
    }
    if (updateStatus === DISPLAY_REASON) {
      element.querySelector('.show-reason').classList.add('hide')
      element.querySelector('.hide-reason').classList.remove('hide')
      element.querySelector('.display_status').value = DISPLAY_REASON
      return
    }
  }
})();
