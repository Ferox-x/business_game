import React from "react"
import "./coordinatorComponentsStyle/coordinatorCodeField.scss"
import "./coordinatorComponentsStyle/coordinatorCode.scss"
import {useClipboard} from "use-clipboard-copy"
import {useDispatch} from "react-redux"
import {NoticeService} from "../../../../../services/noticeService"

function CoordinatorCode({code, update}) {
  const clipboard = useClipboard()

  const dispatch = useDispatch()

  function copyCode() {
    clipboard.copy(code)
    new NoticeService(dispatch).addInfoNotice("Код успешно скопирован!")
  }

  return (
    <div className={"coordinator_code"}>
      <div className="coordinator_code__field">
        <p className="coordinator_code__field_text">
          {code}
        </p>
        <div className="coordinator_code__container">
          <button
            onClick={update}
            className="coordinator_code__container_button button_update_code btn_reset"
          >
            Обновить код
          </button>
          <button
            onClick={copyCode}
            className="coordinator_code__container_button button_copy_code btn_reset"
          >
            Коп. код
          </button>
        </div>
      </div>
    </div>
  )
}

export default CoordinatorCode
