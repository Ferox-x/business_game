import React from "react"
import "./styles/title.css"

function Title({ title, ...props }) {
	return <div className="bs_title">{title}</div>
}

export default Title
