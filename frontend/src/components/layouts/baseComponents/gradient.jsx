import React from "react"
import "../styles/gradient.scss"

function Gradient({ children, ...props }) {
	return <div className="gradient">{children}</div>
}

export default Gradient
