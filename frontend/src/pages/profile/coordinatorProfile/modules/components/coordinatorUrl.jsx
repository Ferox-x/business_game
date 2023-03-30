import React from "react"
import "./coordinatorComponentsStyle/coordinatorCodeField.scss"
import "./coordinatorComponentsStyle/coordinatorUrl.scss"
import {urls} from "../../../../../urls"
import {useClipboard} from "use-clipboard-copy"
import {useDispatch} from "react-redux"
import {NoticeService} from "../../../../../services/noticeService"

function CoordinatorUrl({code, props}) {
  const clipboard = useClipboard()

  const dispatch = useDispatch()

  const url =
    window.location.protocol +
    "//" +
    window.location.hostname +
    ":" +
    window.location.port +
    urls.signUp +
    "/" +
    code

  function copyUrl() {
    clipboard.copy(url)
    new NoticeService(dispatch).addInfoNotice("Ссылка успешно скопирована!")
  }

  return (
    <div className={"coordinator_code"}>
      <div className="coordinator_code__field">
        <p className="coordinator_code__field_text">
          {url}
        </p>
        <div className="coordinator_code__container">
          <button
            onClick={copyUrl}
            className="coordinator_code__container_button button_link_code btn_reset"
          >
            Коп. ссылку
          </button>
        </div>
      </div>
    </div>
  )
}

export default CoordinatorUrl
