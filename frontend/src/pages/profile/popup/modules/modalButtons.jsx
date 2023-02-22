import React from "react"
import "../modules/modalStyles/modalButtons.scss"
import ModalButtonUpdate from "./modalButtonUpdate"
import ModalButtonCode from "./modalButtonCode"
import ModalButtonLink from "./modalButtonLink"

function ModalButtons(props) {
	return (
		<div className={"modal_buttons"}>
			<ModalButtonUpdate />
			<ModalButtonCode />
			<ModalButtonLink />
		</div>
	)
}

export default ModalButtons
