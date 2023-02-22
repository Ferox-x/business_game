import React from "react"
import Header from "./baseComponents/header"
import BaseContainer from "./baseComponents/BaseContainer"

function Layout({ children, ...props }) {
	return (
		<>
			<Header capacity={false} />
			<BaseContainer>{children}</BaseContainer>
		</>
	)
}

export default Layout
