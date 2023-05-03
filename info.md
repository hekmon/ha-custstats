# Home Assistant Custom Integration Statistics

[![Validate with HACS](https://github.com/hekmon/ha-custstats/actions/workflows/hacs.yml/badge.svg)](https://github.com/hekmon/ha-custstats/actions/workflows/hacs.yml)
[![Validate with hassfest](https://github.com/hekmon/ha-custstats/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/hekmon/ha-custstats/actions/workflows/hassfest.yaml)

This integration allows you to track installations statistics for Home Assistant custom integrations.

See [example](https://github.com/hekmon/ha-custstats/raw/v1.0.1/res/rtetempo_svc.png).

## Prerequisites

In order to work, the integration you want to track installation statistics must exist within the Home Assistant custom integrations [statistics file](https://analytics.home-assistant.io/custom_integrations.json). To be part of this file, custom integration must have been declared to the official [Home Assistant Brands repository](https://github.com/home-assistant/brands).

Also, do not forget users can opt-out from analytics. Therefor, you will only see installation statistics from users who have opt-in for [usage analytics](https://www.home-assistant.io/integrations/analytics/#usage-analytics).

## Configuration

Once the integration has been installed and Home Assistant restarted, navigate to the integrations page, select the `Add Integration` button and search for `Custom Integration Stats`. Once the configuration modal opens up, put the integration domain of the integration your want statistics for. If you are unsure of the integration domain, check the [stats file](https://analytics.home-assistant.io/custom_integrations.json) for the integration your are looking for.

If you want to track more than one custom integration, simply repeat the process.
