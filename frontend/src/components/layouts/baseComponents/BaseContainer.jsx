import React from "react"
import "../styles/baseContainer.scss"

function BaseContainer({ children, ...props }) {
	return <div className={"base_container"}>{children}</div>
}

export default BaseContainer
