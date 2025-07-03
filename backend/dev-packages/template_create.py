# %% 
# create siteplan and landscape template and config file
from siteplan_qualitycontrol.company_config import seg_siteplan_template_generate, hpd_landscape_template_generate
seg_siteplan_template_generate()
hpd_landscape_template_generate()

# %% 
# create number templates
from siteplan_qualitycontrol.images import numbers_generate
numbers_generate()

# %%
# create keynote templates
from siteplan_qualitycontrol.images import keynote_template_generate
keynote_template_generate()

# %%
# create arrow tip template
from siteplan_qualitycontrol.images import arrow_tip_template_generate
arrow_tip_template_generate()

# %%
# create letter template
from siteplan_qualitycontrol.images import letters_generate
letters_generate()