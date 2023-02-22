import React from "react"
import "../modules/modalStyles/modalButtonLink.scss"
import ModalSpanText from "./modalSpanText"

function ModalButtonUpdate(props) {
	return (
		<div className={"modal_button_coordinator_container"}>
			<div className={"modal_button_coordinator_link"}></div>
			<ModalSpanText modal={{ span: "Коп. ссылку" }} />
		</div>
	)
}

export default ModalButtonUpdate
