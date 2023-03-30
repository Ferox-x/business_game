import React, { useEffect, useState } from "react"
import BurgerNotMobile from "./burgerNotMobile"
import BurgerMobile from "./burgerMobile"

function Burger({ burgerState, hide }) {
	const [width, setWidth] = useState(window.innerWidth)

	useEffect(() => {
		const handleResize = (event) => {
			setWidth(event.target.innerWidth)
		}
		window.addEventListener("resize", handleResize)
	}, [])

	return (
		<>
			{width > 700 ? (
				<>
					<BurgerNotMobile burgerState={burgerState} hide={hide} />
				</>
			) : (
				<BurgerMobile burgerState={burgerState} hide={hide} />
			)}
		</>
	)
}

export default Burger
