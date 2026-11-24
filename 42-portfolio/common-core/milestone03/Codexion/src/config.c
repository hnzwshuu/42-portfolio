/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   config.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: shanazaw <shanazaw@student.42tokyo.jp>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/03 12:00:00 by shanazaw          #+#    #+#             */
/*   Updated: 2026/10/16 13:05:24 by shanazaw         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	duration_valid(t_time value)
{
	return (value >= 0 && value <= (t_time)INT_MAX * 1000);
}

int	config_valid(const t_config *conf)
{
	if (!conf || conf->count < 1 || conf->required < 0
		|| (conf->edf != 0 && conf->edf != 1))
		return (0);
	return (duration_valid(conf->burnout) && duration_valid(conf->compile)
		&& duration_valid(conf->debug) && duration_valid(conf->refactor)
		&& duration_valid(conf->cooldown));
}
