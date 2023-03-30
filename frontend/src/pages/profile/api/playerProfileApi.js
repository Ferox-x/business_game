import { getAxiosInstanceAuth } from "../../../actions/axios_config"

export class PlayerInfo {
	constructor(dispatch) {
		this.dispatch = dispatch
	}

	async getPlayerInfo() {
		const axiosInstanceAuth = getAxiosInstanceAuth()

		return await axiosInstanceAuth.get("api/player/retrieve").then((response) => {
			if (response.status === 200) {
				this.dispatch({
					type: "SET_PLAYER",
					payload: response.data,
				})
			}
			return response
		})
	}
	async getData() {
		const axiosInstanceAuth = getAxiosInstanceAuth()

		return await axiosInstanceAuth
			.get("/api/player/attributes/value")
			.then((response) => {
				this.dispatch({
					type: "SET_PLAYER_ATTRIBUTES",
					payload: response.data,
				})
				return response
			})
	}
}
