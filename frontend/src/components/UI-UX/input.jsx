import React from "react"
import "./styles/input.css"

function Input({ type, placeholder, value, setValue, image, ...props }) {
	let backgroundImg

	switch (image) {
		case "email":
			backgroundImg = "bs_input__email"
			break
		case "password":
			backgroundImg = "bs_input__password"
			break
		case "password2":
			backgroundImg = "bs_input__password2"
			break
		case "invite_code":
			backgroundImg = "bs_input__invite_code"
			break
	}

	return (
		<input
			className={"bs_input bs_input_background " + backgroundImg}
			type={type}
			placeholder={placeholder}
			value={value}
			onChange={(event) => setValue(event.target.value)}
		/>
	)
}

export default Input
