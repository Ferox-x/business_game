import React from "react"
import "./coordinatorComponentsStyle/coordinatorCodeField.scss"
import "./coordinatorComponentsStyle/coordinatorCode.scss"
import { useClipboard } from "use-clipboard-copy"

function CoordinatorCode({ code, update }) {
	const clipboard = useClipboard()

	function copyCode() {
		clipboard.copy(code)
	}

	return (
		<div className={"coordinator_code"}>
			<div className="coordinator_code_field">
				{code}
				<div className="coordinator_buttons_container">
					<button
						onClick={update}
						className="coordinator_button button_update_code btn_reset"
					>
						Обновить код
					</button>
					<button
						onClick={copyCode}
						className="coordinator_button button_copy_code btn_reset"
					>
						Коп. код
					</button>
				</div>
			</div>
		</div>
	)
}

export default CoordinatorCode
