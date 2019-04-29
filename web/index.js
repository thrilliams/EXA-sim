$.ajax({
	type: 'GET',
	url: '../level.json',
	success: async data => {
		window.level = data
		for (var i = 0; i < level.exas.length; i++) {
			$.ajax({
				type: 'GET',
				url: '../' + level.exas[i],
				success: data => {
					level.exas[i] = data.split('\n')
				},
				async: false
			})
		}
		while (window.sim === undefined) {
			await new Promise(resolve => { setTimeout(_ => resolve(), 10) })
			console.log('waiting...')
		}
		new sim.Level(level)
	}
})