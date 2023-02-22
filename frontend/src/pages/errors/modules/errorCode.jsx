import React from "react"
import "./errorStyles/errorCode.scss"

function ErrorCode(props) {
	return <p className="error_code">{props.error.code}</p>
}

export default ErrorCode
