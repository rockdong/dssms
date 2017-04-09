						<script>
						function demo_create() {
							var ref = $('#jstree_demo').jstree(true),
								sel = ref.get_selected();
							if(!sel.length) { return false; }
							sel = sel[0];
							sel = ref.create_node(sel, {"type":"file"});
							if(sel) {
								ref.edit(sel);
							}
						};
						function demo_rename() {
							var ref = $('#jstree_demo').jstree(true),
								sel = ref.get_selected();
							if(!sel.length) { return false; }
							sel = sel[0];
							ref.edit(sel);
						};
						function demo_delete() {
							var ref = $('#jstree_demo').jstree(true),
								sel = ref.get_selected();
							if(!sel.length) { return false; }
							ref.delete_node(sel);
						};
						$(function () {
							var to = false;
							$('#demo_q').keyup(function () {
								if(to) { clearTimeout(to); }
								to = setTimeout(function () {
									var v = $('#demo_q').val();
									$('#jstree_demo').jstree(true).search(v);
								}, 250);
							});

							$('#jstree_demo')
								.jstree({
									"core" : {
										"animation" : 0,
										"check_callback" : true,
										'force_text' : true,
										"themes" : { "stripes" : true },
										'data' : {
											'url' : function (node) {
												return node.id === '#' ? '/static/3.3.4/assets/ajax_demo_roots.json' : '/static/3.3.4/assets/ajax_demo_children.json';
											},
											'data' : function (node) {
												return { 'id' : node.id };
											}
										}
									},
									"types" : {
										"#" : { "max_children" : 1, "max_depth" : 4, "valid_children" : ["root"] },
										"root" : { "icon" : "/static/3.3.4/assets/images/tree_icon.png", "valid_children" : ["default"] },
										"default" : { "valid_children" : ["default","file"] },
										"file" : { "icon" : "glyphicon glyphicon-file", "valid_children" : [] }
									},
									"plugins" : [ "contextmenu", "dnd", "search", "state", "types", "wholerow" ]
								});
						});
						</script>