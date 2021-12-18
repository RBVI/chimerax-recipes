from chimerax.core.utils import string_to_attr
attr_names = set()
numeric_attr_names = set()
for m in session.models:
	if hasattr(m, 'viewdockx_data'):
		for k, v in m.viewdockx_data.items():
			attr_name = string_to_attr(k, prefix='vdx_')
			if attr_name not in attr_names:
				try:
					x = eval(v)
				except:
					kw = {}
					x = v
				else:
					if isinstance(x, (float, int)):
						kw = { 'attr_type': type(x) }
						numeric_attr_names.add(attr_name)
					else:
						kw = {}
						x = v
				from chimerax.atomic import Structure
				Structure.register_attr(session, attr_name, "ViewDockX attribute script", **kw)
				attr_names.add(attr_name)
			elif attr_name in numeric_attr_names:
				x = eval(v)
			else:
				x = v
			setattr(m, attr_name, x)
session.logger.info("The following numeric ViewDockX attributes were registered: %s" % ", ".join(sorted(list(numeric_attr_names))))
session.logger.info("The following non-numeric ViewDockX attributes were registered: %s" % ", ".join(sorted(list(attr_names - numeric_attr_names))))
