import React from "react"
import BackgroundMain from "../../components/layouts/baseComponents/background_main"
import Logo from "../../components/UI-UX/logo"
import Footer from "../../components/layouts/baseComponents/footer"
import Gradient from "../../components/layouts/baseComponents/gradient"

function AuthPage100Vh({ children, ...props }) {
	return (
		<Gradient>
			<div className="container_auth">
				<BackgroundMain />
				<div className="auth_content">
					<div className="logo_container">
						<Logo />
					</div>
					{children}
				</div>
			</div>
			<Footer />
		</Gradient>
	)
}

export default AuthPage100Vh
