import React from "react"
import "./errorStyles/errorSpan.scss"

function SpanText(props) {
	return <span className={"error_span"}>{props.error.text}</span>
}

export default SpanText
