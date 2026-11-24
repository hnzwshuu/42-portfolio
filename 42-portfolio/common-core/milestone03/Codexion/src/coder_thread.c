/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder_thread.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:05:18 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static t_sim	*lock_thread_sim(t_coder *coder)
{
	if (!coder_valid(coder))
	{
		boundary_error("coder thread: invalid context", EINVAL);
		return (NULL);
	}
	if (!sim_lock(coder->sim))
		return (NULL);
	return (coder->sim);
}

void	*coder_main(void *arg)
{
	t_coder	*coder;
	t_sim	*sim;

	coder = arg;
	sim = lock_thread_sim(coder);
	if (!sim)
		return (arg);
	if (wait_ready(sim) && pause_until(sim,
			deadline_after(sim, sim->start, coder->initial_delay)))
	{
		if (sim->capacity == 1)
			single_coder(coder);
		else
			coder_loop(coder);
	}
	if (!sim_unlock(sim))
		return (arg);
	return (NULL);
}
