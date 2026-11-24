/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:05:55 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static t_time	next_deadline(t_sim *sim)
{
	t_time	deadline;
	t_time	candidate;
	int		index;

	deadline = deadline_after(sim, sim->coders[0].last_start,
			sim->conf.burnout);
	index = 1;
	while (index < sim->conf.count)
	{
		candidate = deadline_after(sim, sim->coders[index].last_start,
				sim->conf.burnout);
		if (candidate < 0)
			return (-1);
		if (candidate < deadline)
			deadline = candidate;
		index++;
	}
	return (deadline);
}

void	*monitor_main(void *arg)
{
	t_sim	*sim;
	t_time	now;
	int		index;

	sim = arg;
	if (!sim_valid(sim) || !sim_lock(sim))
		return (arg);
	wait_ready(sim);
	while (!sim->stopped)
	{
		now = now_us(sim);
		index = expired_coder(sim, now);
		if (index >= 0)
		{
			log_burnout(sim, index, now);
			sim_stop(sim);
		}
		else
			wait_until(sim, &sim->watch, next_deadline(sim));
	}
	if (!sim_unlock(sim))
		return (arg);
	return (NULL);
}
