import React from "react"
import "./modules/errorStyles/error.scss"
import ErrorCode from "./modules/errorCode"
import SpanText from "./modules/spanText"
import Button from "../../components/UI-UX/button"
import { useNavigate } from "react-router-dom"
import { urls } from "../../urls"
import LayoutGradient from "../../components/layouts/layoutGradient"

function Error404(props) {
	const navigate = useNavigate()

	function redirectToMainPage() {
		navigate(urls.mainPage)
	}

	return (
		<LayoutGradient>
			<div className="error_container">
				<div className="error_section">
					<div className="error_code_content">
						<ErrorCode error={{ code: "403" }} />
						<SpanText error={{ text: "Нет прав доступа" }} />
					</div>
					<div className="error_button_container">
						<Button action={redirectToMainPage} children={"На главную"} />
					</div>
				</div>
			</div>
		</LayoutGradient>
	)
}

export default Error404
