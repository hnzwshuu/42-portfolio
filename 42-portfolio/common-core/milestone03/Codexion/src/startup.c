/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   startup.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:06:14 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

t_time	initial_delay(t_config *conf, int index)
{
	t_time	slot;
	int		rank;

	if (!conf || index < 0 || index >= conf->count)
	{
		boundary_error("initial delay: invalid config/index", index);
		return (-1);
	}
	if (conf->count == 1)
		return (0);
	if (conf->count % 2 == 0)
		return ((index % 2) * (conf->compile + conf->cooldown));
	slot = (conf->compile + conf->cooldown + conf->count / 2 - 1)
		/ (conf->count / 2);
	rank = index / 2;
	if (index % 2)
		rank += conf->count / 2 + 1;
	return (rank * slot);
}

static void	initial_requests(t_sim *sim)
{
	int	rank;
	int	index;
	int	evens;

	if (sim->conf.count == 1)
		return ;
	evens = sim->conf.count / 2 + sim->conf.count % 2;
	rank = 0;
	while (rank < sim->conf.count)
	{
		if (rank < evens)
			index = rank * 2;
		else
			index = (rank - evens) * 2 + 1;
		if (!queue_request(&sim->coders[index]))
			return ;
		rank++;
	}
}

void	prepare_start(t_sim *sim)
{
	int	index;

	if (!sim_valid(sim) || sim->phase != SIM_RUNNING || sim->ready)
	{
		sim_error(sim, "start: invalid lifecycle", EINVAL);
		return ;
	}
	initial_requests(sim);
	if (sim->stopped)
		return ;
	sim->start = now_us(sim);
	if (sim->start < 0)
		return ;
	index = 0;
	while (index < sim->conf.count)
	{
		sim->coders[index].last_start = sim->start;
		index++;
	}
	sim->ready = 1;
	sim_notify(sim, 0);
	sim_notify(sim, 1);
}
