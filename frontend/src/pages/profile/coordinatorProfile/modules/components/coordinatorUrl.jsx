import React from "react"
import "./coordinatorComponentsStyle/coordinatorCodeField.scss"
import "./coordinatorComponentsStyle/coordinatorUrl.scss"
import { urls } from "../../../../../urls"
import { useClipboard } from "use-clipboard-copy"

function CoordinatorUrl({ code, props }) {
	const clipboard = useClipboard()

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
	}

	return (
		<div className={"coordinator_code"}>
			<div className="coordinator_code_field">
				{url}
				<div className="coordinator_buttons_container">
					<button
						onClick={copyUrl}
						className="coordinator_button button_link_code btn_reset"
					>
						Коп. ссылку
					</button>
				</div>
			</div>
		</div>
	)
}

export default CoordinatorUrl
