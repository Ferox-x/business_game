import React from "react"
import "./modalStyles/modalSpanText.scss"

function ModalSpanText(props) {
	return <span className={"modal_span_text"}>{props.modal.span}</span>
}

export default ModalSpanText
