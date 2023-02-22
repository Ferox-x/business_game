import React from "react"
import "./popup.scss"
import ModalCoordinatorCodeSection from "./modules/modalCoordinatorCodeSection"
import ModalButtons from "./modules/modalButtons"

function Popup({ popUpState, hide, ...props }) {
	let popUpStateClass

	switch (popUpState) {
		case 0:
			popUpStateClass = "popup_hidden"
			break
		case 1:
			popUpStateClass = "popup_open"
			break
	}

	return (
		<div className={"popup " + popUpStateClass}>
			<div className="popup_container">
				<button onClick={hide} className={"btn_reset button_close_popup"}></button>
				<div className="popup_coordinator_body">
					<ModalCoordinatorCodeSection />
					<ModalButtons />
				</div>
			</div>
		</div>
	)
}

export default Popup
