import React from "react"
import Gradient from "./baseComponents/gradient"
import Header from "./baseComponents/header"
import BaseContainer from "./baseComponents/BaseContainer"

function LayoutGradient({ children, ...props }) {
	return (
		<Gradient>
			<Header capacity={true} />
			<BaseContainer>{children}</BaseContainer>
		</Gradient>
	)
}

export default LayoutGradient
