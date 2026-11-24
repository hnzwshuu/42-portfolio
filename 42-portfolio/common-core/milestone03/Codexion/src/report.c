/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   report.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:06:12 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	report_error(t_sim *sim)
{
	const char	*message;
	int			code;
	int			failed;
	int			locked;

	if (!sim)
		return ;
	locked = (sim->phase == SIM_RUNNING);
	if (locked && !sim_lock(sim))
		return ;
	message = sim->error;
	code = sim->error_code;
	failed = sim->failed;
	if (locked)
		sim_unlock(sim);
	if (failed)
	{
		if (!message)
			message = "unspecified simulation failure";
		boundary_error(message, code);
	}
}
