import React from "react"
import "../modules/modalStyles/modalButtonUpdate.scss"
import ModalSpanText from "./modalSpanText"

function ModalButtonUpdate(props) {
	return (
		<div className={"modal_button_coordinator_container"}>
			<div className={"modal_button_coordinator_update"}></div>
			<ModalSpanText modal={{ span: "Обновить код" }} />
		</div>
	)
}

export default ModalButtonUpdate
