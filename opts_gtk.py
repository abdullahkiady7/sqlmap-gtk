#!/usr/bin/env python3
#
# 2019-05-14 19:44:19

from widgets import (g, Box, Frame, label)
from widgets import (HORIZONTAL, VERTICAL)


class Notebook(g.Notebook):
  '''
  m: model.Model
  最大的宽应该是由最长的 request定制的第一行 决定

  如果所有标签页全用ScrolledWindow的话, UI的尺寸(size)会变得很小
  以"Other"标签的height作为标准高,
  高于此height的标签页使用ScrolledWindow, 显示滚动条
  '''
  def __init__(self, m, handlers):
    super().__init__()

    self.m = m
    self._handlers = handlers
    # OPTIONS - Inject, Request, Enumerate, File, Other
    page1_setting = self.build_page1_setting(m)
    page1_request = self.build_page1_request()
    page1_enumeration = self.build_page1_enumeration()
    page1_file = self.build_page1_file()
    page1_other = self.build_page1_other()
    page1_tamper = self.build_page1_tamper(m)

    _ = m._
    self.append_page(page1_setting, label.new_with_mnemonic(_('Inject(_Q)')))
    self.append_page(page1_request, label.new_with_mnemonic(_('Request(_W)')))
    self.append_page(page1_enumeration, label.new_with_mnemonic(_('Enumerate(_E)')))
    self.append_page(page1_file, label.new_with_mnemonic(_('File(_R)')))
    self.append_page(page1_other, label.new_with_mnemonic(_('Other(_T)')))
    self.append_page(page1_tamper, label.new_with_mnemonic(_('Tamper(_Y)')))

  def cb_single(self, widget, ckbtn):
    if widget.get_active():
      ckbtn.set_active(False)

  def optimize_area_controller(self, button):
    m = self.m
    if m._optimize_area_turn_all_ckbtn.get_active():
      m._optimize_area_keep_alive_ckbtn.set_active(False)
      m._optimize_area_null_connect_ckbtn.set_active(False)
      m._request_area_proxy_ckbtn.set_active(False)

      m._optimize_area_keep_alive_ckbtn.set_sensitive(False)
      m._optimize_area_null_connect_ckbtn.set_sensitive(False)
      m._request_area_proxy_ckbtn.set_sensitive(False)
    else:
      m._optimize_area_keep_alive_ckbtn.set_sensitive(True)
      m._optimize_area_null_connect_ckbtn.set_sensitive(True)
      m._request_area_proxy_ckbtn.set_sensitive(True)

  def build_page1_setting(self, m):
    box = Box(orientation=VERTICAL)

    _row0 = Box()
    _sqlmap_path_label = label.new(m._('sqlmap path:'))
    m._sqlmap_path_entry.set_text('sqlmap')
    m._sqlmap_path_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._sqlmap_path_entry]
    )

    _row0.pack_start(_sqlmap_path_label, False, True, 5)
    _row0.pack_start(m._sqlmap_path_entry, True, True, 5)
    _row0.pack_start(m._sqlmap_path_chooser, False, True, 5)

    _row1 = Box()
    _inject_area = self.build_page1_setting_inject(self.m)
    _detection_area = self.build_page1_setting_detection(self.m)
    _tech_area = self.build_page1_setting_tech(self.m)

    _row1.pack_start(_inject_area, False, True, 5)
    _row1.pack_start(_detection_area, True, True, 5)
    _row1.pack_start(_tech_area, False, True, 5)

    _row2 = Box()
    # _tamper_area = self._build_page1_setting_tamper(self.m)
    _optimize_area = self.build_page1_setting_optimize(self.m)
    _offen_area = self.build_page1_setting_offen(self.m)
    _hidden_area = self.build_page1_setting_hidden(self.m)

    # _row2.pack_start(_tamper_area, False, True, 5)
    _row2.pack_start(_optimize_area, False, True, 5)
    _row2.pack_start(_offen_area, False, True, 5)
    _row2.pack_start(_hidden_area, False, True, 5)

    box.pack_start(_row0, False, True, 5)
    box.pack_start(_row1, False, True, 0)
    box.pack_start(_row2, False, True, 5)

    scrolled = g.ScrolledWindow()
    scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    scrolled.add(box)
    return scrolled

  def build_page1_setting_inject(self, m):
    _f = Frame.new(m._('Injection'))
    _boxes = [Box() for _ in range(13)]

    m._inject_area_param_ckbtn.connect(
      'clicked',
      self.cb_single, m._detection_area_level_ckbtn)
    i = 0
    _boxes[i].pack_start(m._inject_area_param_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._inject_area_param_entry, True, True, 5)

    _ = g.ListStore(str)
    for _data in (["GET"], ["POST"], ["URI"],
                  ["Cookie"], ["User-Agent"], ["Referer"],
                  ["Host"], ["(custom) POST"], ["(custom) HEADER"]):
      _.append(_data)

    m._inject_area_param_filter_combobox.set_model(_)
    m._inject_area_param_filter_combobox.set_entry_text_column(0)
    m._inject_area_param_filter_combobox.set_active(0)
    m._inject_area_param_filter_combobox.get_child().set_editable(False)
    i += 1
    _boxes[i].pack_start(m._inject_area_param_filter_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._inject_area_param_filter_combobox, True, True, 5)

    # set_active(True)为选中状态
    m._inject_area_skip_static_ckbtn.set_active(True)
    i += 1
    _boxes[i].pack_start(m._inject_area_skip_static_ckbtn, False, True, 5)
    i += 1
    _boxes[i].pack_start(m._inject_area_skip_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._inject_area_skip_entry, True, True, 5)
    i += 1
    _boxes[i].pack_start(m._inject_area_param_exclude_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._inject_area_param_exclude_entry, True, True, 5)
    i += 1
    _boxes[i].pack_start(m._inject_area_prefix_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._inject_area_prefix_entry, True, True, 5)
    i += 1
    _boxes[i].pack_start(m._inject_area_suffix_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._inject_area_suffix_entry, True, True, 5)

    _ = g.ListStore(str)
    _.append(["postgresql"])
    _.append(["MySQL <version>"])
    _.append(["Microsoft SQL Server <version>"])

    m._inject_area_dbms_combobox.set_model(_)
    m._inject_area_dbms_combobox.set_entry_text_column(0)
    i += 1
    _boxes[i].pack_start(m._inject_area_dbms_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._inject_area_dbms_combobox, True, True, 5)
    i += 1
    _boxes[i].pack_start(m._inject_area_dbms_cred_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._inject_area_dbms_cred_entry, True, True, 5)
    i += 1
    _boxes[i].pack_start(m._inject_area_os_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._inject_area_os_entry, True, True, 5)
    i += 1
    _boxes[i].pack_start(m._inject_area_no_cast_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._inject_area_no_escape_ckbtn, False, True, 5)

    _invalid_label = label.new('payload\'s invalid value:')
    _invalid_label.set_tooltip_text('default:\nTrue: id=13, False: id=-13')
    i += 1
    _boxes[i].pack_start(_invalid_label, False, True, 5)
    _boxes[i].pack_end(m._inject_area_invalid_bignum_ckbtn, False, True, 5)
    i += 1
    _boxes[i].pack_end(m._inject_area_invalid_string_ckbtn, False, True, 5)
    _boxes[i].pack_end(m._inject_area_invalid_logical_ckbtn, False, True, 5)

    _inject_area_opts = Box(orientation=VERTICAL, spacing=3)
    for _ in _boxes:
      _inject_area_opts.add(_)

    _f.add(_inject_area_opts)
    return _f

  def build_page1_setting_detection(self, m):
    _f = Frame.new(m._('Detection'))
    _boxes = [Box() for _ in range(9)]

    m._detection_area_level_ckbtn.connect(
      'clicked',
      self.cb_single, m._inject_area_param_ckbtn)

    _boxes[0].pack_start(m._detection_area_level_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._detection_area_level_scale, True, True, 5)
    _boxes[1].pack_start(m._detection_area_risk_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._detection_area_risk_scale, True, True, 10)
    _boxes[2].pack_start(m._detection_area_str_ckbtn, False, True, 5)
    _boxes[2].pack_end(m._detection_area_str_entry, True, True, 5)
    _boxes[3].pack_start(m._detection_area_not_str_ckbtn, False, True, 5)
    _boxes[3].pack_end(m._detection_area_not_str_entry, True, True, 5)
    _boxes[4].pack_start(m._detection_area_re_ckbtn, False, True, 5)
    _boxes[4].pack_end(m._detection_area_re_entry, True, True, 5)
    _boxes[5].pack_start(m._detection_area_code_ckbtn, False, True, 5)
    _boxes[5].pack_start(m._detection_area_code_entry, False, True, 5)

    m._detection_area_text_only_ckbtn.connect(
      'clicked',
      self.cb_single, m._optimize_area_null_connect_ckbtn)
    m._detection_area_text_only_ckbtn.connect(
      'clicked',
      self.cb_single, m._detection_area_titles_ckbtn)
    m._detection_area_titles_ckbtn.connect(
      'clicked',
      self.cb_single, m._detection_area_text_only_ckbtn)

    _boxes[6].pack_start(m._detection_area_text_only_ckbtn, False, True, 5)
    _boxes[6].pack_start(m._detection_area_titles_ckbtn, True, False, 5)
    _boxes[6].pack_start(m._detection_area_smart_ckbtn, False, True, 5)
    _boxes[7].pack_start(g.Separator.new(HORIZONTAL), True, True, 5)
    # m._detection_area_risk_note.override_background_color(g.StateFlags.NORMAL,
    #                                                       d.RGBA(255, 0, 0, 1))
    _boxes[8].set_spacing(6)
    _boxes[8].pack_start(m._detection_area_level_note, True, True, 5)
    _boxes[8].pack_start(m._detection_area_risk_note, True, True, 5)

    _detection_area_opts = Box(orientation=VERTICAL, spacing=3)
    for _ in _boxes:
      _detection_area_opts.add(_)

    _f.add(_detection_area_opts)
    return _f

  def build_page1_setting_tech(self, m):
    _f = Frame.new(m._('Technique'))
    _boxes = [Box() for _ in range(9)]

    _boxes[0].pack_start(m._tech_area_tech_ckbtn, False, True, 5)
    _boxes[0].pack_end(m._tech_area_tech_entry, False, True, 5)
    _boxes[1].pack_start(m._tech_area_time_sec_ckbtn, False, True, 5)
    _boxes[1].pack_end(m._tech_area_time_sec_entry, False, True, 5)
    _boxes[2].pack_start(m._tech_area_union_col_ckbtn, False, True, 5)
    _boxes[2].pack_end(m._tech_area_union_col_entry, False, True, 5)
    _boxes[3].pack_start(m._tech_area_union_char_ckbtn, False, True, 5)
    _boxes[3].pack_end(m._tech_area_union_char_entry, False, True, 5)
    _boxes[4].pack_start(m._tech_area_union_from_ckbtn, False, True, 5)
    _boxes[4].pack_end(m._tech_area_union_from_entry, False, True, 5)
    _boxes[5].pack_start(m._tech_area_dns_ckbtn, True, True, 5)
    _boxes[5].pack_end(m._tech_area_dns_entry, True, True, 5)
    _boxes[6].pack_start(m._tech_area_second_url_ckbtn, True, True, 5)
    _boxes[6].pack_end(m._tech_area_second_url_entry, True, True, 5)
    _boxes[7].pack_start(m._tech_area_second_req_ckbtn, False, True, 5)

    m._tech_area_second_req_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._tech_area_second_req_entry]
    )

    _boxes[8].pack_end(m._tech_area_second_req_chooser, False, True, 5)
    _boxes[8].pack_end(m._tech_area_second_req_entry, True, True, 5)

    _tech_area_opts = Box(orientation=VERTICAL, spacing=3)
    for _ in _boxes:
      _tech_area_opts.add(_)

    _f.add(_tech_area_opts)
    return _f

  # def _build_page1_setting_tamper(self, m):
  #   '''
  #   frame套box, box再套scroll会出现:
  #   一直按回车出现滚动条后, 光标会下移 直到移出可见区, 原内容不会上移
  #   即内容的显示没有 下滑 滚轮的效果.
  #   '''
  #   _scrolled = g.ScrolledWindow()
  #   _scrolled.set_size_request(300, -1)
  #   _scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
  #   _scrolled.add(m._tamper_area_tamper_view)

  #   m._tamper_frame.add(_scrolled)
  #   return m._tamper_frame

  def build_page1_setting_optimize(self, m):
    _f = Frame.new(m._('Optimize'))
    _boxes = [Box() for _ in range(5)]

    m._optimize_area_turn_all_ckbtn.connect('clicked', self.optimize_area_controller)

    _boxes[0].pack_start(m._optimize_area_turn_all_ckbtn, False, True, 5)

    m._optimize_area_thread_num_ckbtn.connect(
      'clicked',
      self.cb_single, m._optimize_area_predict_ckbtn)
    _boxes[1].pack_start(m._optimize_area_thread_num_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._optimize_area_thread_num_spinbtn, True, True, 5)

    m._optimize_area_predict_ckbtn.connect(
      'clicked',
      self.cb_single, m._optimize_area_thread_num_ckbtn)
    _boxes[2].pack_start(m._optimize_area_predict_ckbtn, False, True, 5)

    m._optimize_area_keep_alive_ckbtn.connect(
      'clicked',
      self.cb_single, m._request_area_proxy_ckbtn)
    _boxes[3].pack_start(m._optimize_area_keep_alive_ckbtn, False, True, 5)

    m._optimize_area_null_connect_ckbtn.connect(
      'clicked',
      self.cb_single, m._detection_area_text_only_ckbtn)
    _boxes[4].pack_start(m._optimize_area_null_connect_ckbtn, False, True, 5)

    _optimize_area_opts = Box(orientation=VERTICAL, spacing=6)
    for _ in _boxes:
      _optimize_area_opts.add(_)

    _f.add(_optimize_area_opts)
    return _f

  def build_page1_setting_offen(self, m):
    _f = Frame.new(m._('Offen'))
    _boxes = [Box() for _ in range(5)]

    _general_area_opts = Box(orientation=VERTICAL, spacing=6)

    m._general_area_verbose_scale.set_value(1.0)

    _boxes[0].pack_start(m._general_area_verbose_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._general_area_verbose_scale, True, True, 5)
    _boxes[1].pack_start(m._general_area_finger_ckbtn, False, True, 5)
    _boxes[2].pack_start(m._general_area_hex_ckbtn, False, True, 5)
    _boxes[3].pack_start(m._general_area_batch_ckbtn, False, True, 5)
    _boxes[4].pack_start(m._misc_area_wizard_ckbtn, False, True, 5)
    for _ in _boxes:
      _general_area_opts.add(_)

    _f.add(_general_area_opts)
    return _f

  def build_page1_setting_hidden(self, m):
    _f = Frame.new(m._('Hidden'))
    _boxes = [Box() for _ in range(6)]
    _ = 0
    _boxes[_].pack_start(m._hidden_area_crack_ckbtn, False, True, 5)
    _boxes[_].pack_start(m._hidden_area_debug_ckbtn, False, True, 5)
    _boxes[_].pack_start(m._hidden_area_profile_ckbtn, False, True, 5)
    _ += 1
    _boxes[_].pack_start(m._hidden_area_disable_precon_ckbtn, False, True, 5)
    _boxes[_].pack_start(m._hidden_area_disable_stats_ckbtn, False, True, 5)
    _ += 1
    _boxes[_].pack_start(m._hidden_area_force_dbms_ckbtn, False, True, 5)
    _boxes[_].pack_start(m._hidden_area_force_dns_ckbtn, False, True, 0)
    _boxes[_].pack_start(m._hidden_area_force_pivoting_ckbtn, False, True, 5)
    _ += 1
    _boxes[_].pack_start(m._hidden_area_smoke_test_ckbtn, False, True, 5)
    _boxes[_].pack_start(m._hidden_area_live_test_ckbtn, False, True, 5)
    _boxes[_].pack_start(m._hidden_area_vuln_test_ckbtn, False, True, 5)
    _ += 1
    _boxes[_].pack_start(m._hidden_area_murphy_rate_ckbtn, False, True, 5)
    _boxes[_].pack_start(m._hidden_area_stop_fail_ckbtn, False, True, 5)
    _boxes[_].pack_start(m._hidden_area_run_case_ckbtn, False, True, 5)
    _ += 1
    _boxes[_].pack_start(m._hidden_area_dummy_ckbtn, False, True, 5)
    _boxes[_].pack_start(m._hidden_area_api_ckbtn, False, True, 5)
    _boxes[_].pack_start(m._hidden_area_taskid_ckbtn, False, True, 5)
    _boxes[_].pack_start(m._hidden_area_database_ckbtn, False, True, 5)

    _hidden_area_opts = Box(orientation=VERTICAL, spacing=5)
    for _ in _boxes:
      _hidden_area_opts.add(_)

    _f.add(_hidden_area_opts)
    return _f

  def build_page1_request(self):
    box = Box(orientation=VERTICAL)

    _boxes = [Box() for _ in range(4)]

    _request_header_area = self.build_page1_request_header(self.m)
    _boxes[0].pack_start(_request_header_area, True, True, 5)

    _request_data_area = self.build_page1_request_data(self.m)
    _boxes[1].pack_start(_request_data_area, True, True, 5)

    _request_custom_area = self.build_page1_request_custom(self.m)
    _boxes[2].pack_start(_request_custom_area, True, True, 5)

    _request_proxy_area = self.build_page1_request_proxy(self.m)
    _boxes[3].pack_start(_request_proxy_area, True, True, 5)

    for _ in _boxes:
      box.pack_start(_, False, True, 5)

    scrolled = g.ScrolledWindow()
    scrolled.set_policy(g.PolicyType.NEVER, g.PolicyType.ALWAYS)
    scrolled.add(box)
    return scrolled

  def build_page1_request_header(self, m):
    _f = Frame.new(m._('HTTP header'))
    _boxes = [Box() for _ in range(3)]

    m._request_area_random_agent_ckbtn.set_active(True)

    _boxes[0].pack_start(m._request_area_random_agent_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._request_area_mobile_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._request_area_user_agent_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._request_area_user_agent_entry, True, True, 5)
    _boxes[1].pack_start(m._request_area_host_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._request_area_host_entry, True, True, 5)
    _boxes[1].pack_start(m._request_area_referer_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._request_area_referer_entry, True, True, 5)
    _boxes[2].pack_start(m._request_area_header_ckbtn, False, True, 5)
    _boxes[2].pack_start(m._request_area_header_entry, True, True, 5)
    _boxes[2].pack_start(m._request_area_headers_ckbtn, False, True, 5)
    _boxes[2].pack_start(m._request_area_headers_entry, True, True, 5)

    _request_header_opts = Box(orientation=VERTICAL, spacing = 5)
    for _ in _boxes:
      _request_header_opts.add(_)

    _f.add(_request_header_opts)
    return _f

  def build_page1_request_data(self, m):
    _f = Frame.new(m._('HTTP data'))
    _boxes = [Box() for _ in range(8)]

    _boxes[0].pack_start(m._request_area_method_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._request_area_method_entry, False, True, 5)
    _boxes[0].pack_start(m._request_area_param_del_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._request_area_param_del_entry, False, True, 5)
    _boxes[0].pack_start(m._request_area_chunked_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._request_area_post_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._request_area_post_entry, True, True, 5)
    _boxes[2].pack_start(g.Separator.new(HORIZONTAL), True, True, 5)
    _boxes[3].pack_start(m._request_area_cookie_ckbtn, False, True, 5)
    _boxes[3].pack_start(m._request_area_cookie_entry, True, True, 5)
    _boxes[3].pack_start(m._request_area_cookie_del_ckbtn, False, True, 5)
    _boxes[3].pack_start(m._request_area_cookie_del_entry, False, True, 5)

    m._request_area_live_cookies_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._request_area_live_cookies_entry]
    )
    m._request_area_load_cookies_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._request_area_load_cookies_entry]
    )

    _boxes[4].pack_start(m._request_area_drop_set_cookie_ckbtn, False, True, 5)
    _boxes[4].pack_start(m._request_area_live_cookies_ckbtn, False, True, 5)
    _boxes[4].pack_start(m._request_area_live_cookies_entry, True, True, 0)
    _boxes[4].pack_start(m._request_area_live_cookies_chooser, False, True, 5)
    _boxes[4].pack_start(m._request_area_load_cookies_ckbtn, False, True, 5)
    _boxes[4].pack_start(m._request_area_load_cookies_entry, True, True, 0)
    _boxes[4].pack_start(m._request_area_load_cookies_chooser, False, True, 5)
    _boxes[5].pack_start(g.Separator.new(HORIZONTAL), True, True, 5)

    m._request_area_auth_file_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._request_area_auth_file_entry]
    )

    _boxes[6].pack_start(m._request_area_auth_type_ckbtn, False, True, 5)
    _boxes[6].pack_start(m._request_area_auth_type_entry, True, True, 5)
    _boxes[6].pack_start(m._request_area_auth_cred_ckbtn, False, True, 5)
    _boxes[6].pack_start(m._request_area_auth_cred_entry, True, True, 5)
    _boxes[6].pack_start(m._request_area_auth_file_ckbtn, False, True, 5)
    _boxes[6].pack_start(m._request_area_auth_file_entry, True, True, 0)
    _boxes[6].pack_start(m._request_area_auth_file_chooser, False, True, 5)

    m._request_area_csrf_retries_entry.set_width_chars(5)

    _boxes[7].pack_start(m._request_area_csrf_method_ckbtn, False, True, 5)
    _boxes[7].pack_start(m._request_area_csrf_method_entry, False, True, 5)
    _boxes[7].pack_start(m._request_area_csrf_retries_ckbtn, False, True, 5)
    _boxes[7].pack_start(m._request_area_csrf_retries_entry, False, True, 5)
    _boxes[7].pack_start(m._request_area_csrf_token_ckbtn, False, True, 5)
    _boxes[7].pack_start(m._request_area_csrf_token_entry, True, True, 5)
    _boxes[7].pack_start(m._request_area_csrf_url_ckbtn, False, True, 5)
    _boxes[7].pack_start(m._request_area_csrf_url_entry, True, True, 5)

    _request_data_opts = Box(orientation=VERTICAL, spacing = 5)
    for _ in _boxes:
      _request_data_opts.add(_)

    _f.add(_request_data_opts)
    return _f

  def build_page1_request_custom(self, m):
    _f = Frame.new(m._('Request custom'))
    _boxes = [Box() for _ in range(3)]

    _boxes[0].pack_start(m._request_area_ignore_timeouts_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._request_area_ignore_redirects_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._request_area_ignore_code_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._request_area_ignore_code_entry, False, True, 5)
    _boxes[0].pack_start(m._request_area_skip_urlencode_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._request_area_force_ssl_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._request_area_hpp_ckbtn, False, True, 5)

    m._request_area_delay_entry.set_width_chars(10)
    m._request_area_timeout_entry.set_width_chars(10)
    m._request_area_timeout_entry.set_text('30')
    m._request_area_retries_entry.set_width_chars(10)
    m._request_area_retries_entry.set_text('3')

    _boxes[1].pack_start(m._request_area_delay_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._request_area_delay_entry, False, True, 5)
    _boxes[1].pack_start(m._request_area_timeout_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._request_area_timeout_entry, False, True, 5)
    _boxes[1].pack_start(m._request_area_retries_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._request_area_retries_entry, False, True, 5)
    _boxes[1].pack_start(m._request_area_randomize_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._request_area_randomize_entry, True, True, 5)

    _boxes[2].pack_start(m._request_area_eval_ckbtn, False, True, 5)
    _boxes[2].pack_start(m._request_area_eval_entry, True, True, 5)

    _request_custom_opts = Box(orientation=VERTICAL, spacing = 5)
    for _ in _boxes:
      _request_custom_opts.add(_)

    _f.add(_request_custom_opts)
    return _f

  def build_page1_request_proxy(self, m):
    _f = Frame.new(m._('Anonymous/Proxy'))
    _boxes = [Box() for _ in range(6)]

    _boxes[0].pack_start(m._request_area_safe_url_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._request_area_safe_url_entry, True, True, 5)
    _boxes[0].pack_start(m._request_area_safe_post_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._request_area_safe_post_entry, True, True, 5)

    m._request_area_safe_req_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._request_area_safe_req_entry]
    )

    _boxes[1].pack_start(m._request_area_safe_req_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._request_area_safe_req_entry, True, True, 0)
    _boxes[1].pack_start(m._request_area_safe_req_chooser, False, True, 5)
    _boxes[1].pack_start(m._request_area_safe_freq_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._request_area_safe_freq_entry, False, True, 5)
    _boxes[2].pack_start(g.Separator.new(HORIZONTAL), True, True, 5)

    m._request_area_proxy_ckbtn.connect(
      'clicked',
      self.cb_single, m._optimize_area_keep_alive_ckbtn)
    m._request_area_proxy_file_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._request_area_proxy_file_entry]
    )

    m._request_area_proxy_freq_entry.set_width_chars(10)
    m._request_area_proxy_port_entry.set_width_chars(10)
    m._request_area_tor_port_entry.set_width_chars(10)

    _boxes[3].pack_start(m._request_area_ignore_proxy_ckbtn, False, True, 5)
    _boxes[3].pack_start(m._request_area_proxy_freq_ckbtn, False, True, 5)
    _boxes[3].pack_start(m._request_area_proxy_freq_entry, False, True, 5)
    _boxes[3].pack_start(m._request_area_proxy_file_ckbtn, False, True, 5)
    _boxes[3].pack_start(m._request_area_proxy_file_entry, True, True, 0)
    _boxes[3].pack_start(m._request_area_proxy_file_chooser, False, True, 5)
    _boxes[4].pack_start(m._request_area_proxy_ckbtn, False, True, 5)
    _boxes[4].pack_start(m._request_area_proxy_ip_label, False, True, 5)
    _boxes[4].pack_start(m._request_area_proxy_ip_entry, True, True, 5)
    _boxes[4].pack_start(m._request_area_proxy_port_label, False, True, 5)
    _boxes[4].pack_start(m._request_area_proxy_port_entry, False, True, 5)
    _boxes[4].pack_start(m._request_area_proxy_username_label, False, True, 5)
    _boxes[4].pack_start(m._request_area_proxy_username_entry, True, True, 5)
    _boxes[4].pack_start(m._request_area_proxy_password_label, False, True, 5)
    _boxes[4].pack_start(m._request_area_proxy_password_entry, True, True, 5)
    _boxes[5].pack_start(m._request_area_tor_ckbtn, False, True, 5)
    _boxes[5].pack_start(m._request_area_tor_port_ckbtn, False, True, 5)
    _boxes[5].pack_start(m._request_area_tor_port_entry, False, True, 5)
    _boxes[5].pack_start(m._request_area_tor_type_ckbtn, False, True, 5)
    _boxes[5].pack_start(m._request_area_tor_type_entry, False, True, 5)
    _boxes[5].pack_start(m._request_area_check_tor_ckbtn, False, True, 5)

    _request_proxy_opts = Box(orientation=VERTICAL, spacing = 5)
    for _ in _boxes:
      _request_proxy_opts.add(_)

    _f.add(_request_proxy_opts)
    return _f

  def build_page1_enumeration(self):
    box = Box(orientation=VERTICAL)

    _boxes = [Box(margin_top = 10, margin_start = 10, margin_end = 10) for _ in range(4)]

    _enum_area = self.build_page1_enumeration_enum(self.m)
    _dump_area = self.build_page1_enumeration_dump(self.m)
    _limit_area = self.build_page1_enumeration_limit(self.m)
    _blind_area = self.build_page1_enumeration_blind(self.m)

    _boxes[0].pack_start(_enum_area, False, True, 10)
    _boxes[0].pack_start(_dump_area, False, True, 10)
    _boxes[0].pack_start(_limit_area, False, True, 10)
    _boxes[0].pack_start(_blind_area, False, True, 10)

    _meta_area = self.build_page1_enumeration_meta(self.m)

    _boxes[1].pack_start(_meta_area, True, True, 10)

    _runsql_area = self.build_page1_enumeration_runsql(self.m)

    _boxes[2].pack_start(_runsql_area, True, True, 10)

    _brute_force_area = self.build_page1_enumeration_brute_force(self.m)

    _boxes[3].pack_start(_brute_force_area, False, True, 10)

    for _ in _boxes:
      box.add(_)

    return box

  def build_page1_enumeration_enum(self, m):
    _f = Frame.new(m._('Enumeration'))
    _grid = g.Grid(column_spacing = 20, margin_left = 5, margin_right = 5)

    for _x in range(len(m._enum_area_opts_ckbtns)):
      for _y in range(len(m._enum_area_opts_ckbtns[_x])):
        _grid.attach(m._enum_area_opts_ckbtns[_x][_y], _x, _y, 1, 1)

    _f.add(_grid)
    return _f

  def build_page1_enumeration_dump(self, m):
    _f = Frame.new(m._('Dump'))
    _dump_area_opts = Box(spacing=6)

    # for padding in HORIZONTAL
    _dump_area_opts_cols = Box(orientation=VERTICAL)

    _dump_area_opts_cols.add(m._dump_area_dump_ckbtn)
    _dump_area_opts_cols.add(m._dump_area_repair_ckbtn)
    _dump_area_opts_cols.add(m._dump_area_statements_ckbtn)
    _ = Box()
    _.pack_start(m._dump_area_search_ckbtn, False, True, 0)
    _.pack_start(m._dump_area_no_sys_db_ckbtn, True, False, 0)
    _dump_area_opts_cols.add(_)
    _dump_area_opts_cols.add(m._dump_area_dump_all_ckbtn)

    _dump_area_opts.pack_start(_dump_area_opts_cols, False, True, 10)

    _f.add(_dump_area_opts)
    return _f

  def build_page1_enumeration_limit(self, m):
    _f = Frame.new(m._('Limit'))
    _boxes = [Box() for _ in range(2)]

    _boxes[0].pack_start(m._limit_area_start_ckbtn, False, True, 5)
    _boxes[0].pack_end(m._limit_area_start_entry, False, True, 5)
    # _boxes[0].pack_start(label.new('行'), False, True, 5)
    _boxes[1].pack_start(m._limit_area_stop_ckbtn, False, True, 5)
    _boxes[1].pack_end(m._limit_area_stop_entry, False, True, 5)
    # _boxes[1].pack_start(label.new('行'), False, True, 5)

    _limit_area_opts = Box(orientation=VERTICAL)
    for _ in _boxes:
      _limit_area_opts.pack_start(_, False, True, 10)

    _f.add(_limit_area_opts)
    return _f

  def build_page1_enumeration_blind(self, m):
    _f = Frame.new(m._('Blind inject options'))
    _boxes = [Box() for _ in range(2)]

    _boxes[0].pack_start(m._blind_area_first_ckbtn, False, True, 5)
    _boxes[0].pack_end(m._blind_area_first_entry, False, True, 5)
    # _boxes[0].pack_start(label.new('个字符'), False, True, 5)
    _boxes[1].pack_start(m._blind_area_last_ckbtn, False, True, 5)
    _boxes[1].pack_end(m._blind_area_last_entry, False, True, 5)
    # _boxes[1].pack_start(label.new('个字符'), False, True, 5)

    _blind_area_opts = Box(orientation=VERTICAL)
    for _ in _boxes:
      _blind_area_opts.pack_start(_, False, True, 10)

    _f.add(_blind_area_opts)
    return _f

  def build_page1_enumeration_meta(self, m):
    _f = Frame.new(m._('DB, Table, Column name...'))
    _boxes = [Box() for _ in range(3)]

    _boxes[0].pack_start(m._meta_area_D_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._meta_area_D_entry, True, True, 5)
    _boxes[0].pack_start(m._meta_area_T_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._meta_area_T_entry, True, True, 5)
    _boxes[0].pack_start(m._meta_area_C_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._meta_area_C_entry, True, True, 5)
    _boxes[1].pack_start(m._meta_area_U_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._meta_area_U_entry, True, True, 5)
    _boxes[1].pack_start(m._meta_area_X_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._meta_area_X_entry, True, True, 5)
    _boxes[1].pack_start(m._meta_area_pivot_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._meta_area_pivot_entry, True, True, 5)
    _boxes[2].pack_start(m._meta_area_where_ckbtn, False, True, 5)
    _boxes[2].pack_start(m._meta_area_where_entry, True, True, 5)

    _meta_area_opts = Box(orientation=VERTICAL)
    for _ in _boxes:
      _meta_area_opts.pack_start(_, False, True, 5)

    _f.add(_meta_area_opts)
    return _f

  def build_page1_enumeration_runsql(self, m):
    _f = Frame.new(m._('Execute SQL'))
    _boxes = [Box() for _ in range(2)]

    _boxes[0].pack_start(m._runsql_area_sql_query_ckbtn, False, True, 10)
    _boxes[0].pack_start(m._runsql_area_sql_query_entry, True, True, 10)

    m._runsql_area_sql_file_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._runsql_area_sql_file_entry]
    )

    _boxes[1].pack_start(m._runsql_area_sql_shell_ckbtn, False, True, 10)
    _boxes[1].pack_start(m._runsql_area_sql_file_ckbtn, False, True, 10)
    _boxes[1].pack_start(m._runsql_area_sql_file_entry, True, True, 0)
    _boxes[1].pack_start(m._runsql_area_sql_file_chooser, False, True, 10)

    _runsql_area_opts = Box(orientation=VERTICAL)
    for _ in _boxes:
      _runsql_area_opts.pack_start(_, False, True, 5)

    _f.add(_runsql_area_opts)
    return _f

  def build_page1_enumeration_brute_force(self, m):
    _f = Frame.new(m._('Brute force'))
    _brute_force_area_opts = Box(orientation=VERTICAL)

    _row1 = Box()
    _row1.pack_start(label.new(m._('check existence of:')), False, True, 10)
    _row1.pack_start(m._brute_force_area_common_tables_ckbtn, False, True, 0)
    _row1.pack_start(m._brute_force_area_common_columns_ckbtn, False, True, 5)
    _row1.pack_start(m._brute_force_area_common_files_ckbtn, False, True, 0)

    _brute_force_area_opts.pack_start(_row1, False, True, 5)

    _f.add(_brute_force_area_opts)
    return _f

  def build_page1_file(self):
    box = Box(orientation=VERTICAL, spacing=6)

    _file_note = label(
        label = 'Note: only if stacked query(堆查询注入) worked, '
                'these functions below can be used except udf!',
        halign = g.Align.START,
        margin_start = 16)
    # http://www.sqlinjection.net/stacked-queries/
    # https://www.cnblogs.com/hongfei/p/3895980.html
    _file_note.set_tooltip_text(
        'stacked query: MySQL/PHP - no(but supported by MySQL with other API)\n'
        '               SQL Server/Any API - yes\n'
        '               PostgreSQL/PHP - yes\n'
        '               Oracle/Any API - no')

    _boxes = [Box(margin_top = 10, margin_start = 10, margin_end = 10) for _ in range(4)]

    _file_read_area = self.build_page1_file_read(self.m)
    _file_write_area = self.build_page1_file_write(self.m)
    _os_access_area = self.build_page1_file_os_access(self.m)
    _registry_area = self.build_page1_file_os_registry(self.m)

    _boxes[0].pack_start(_file_read_area, True, True, 6)
    _boxes[1].pack_start(_file_write_area, True, True, 6)
    _boxes[2].pack_start(_os_access_area, True, True, 6)
    _boxes[3].pack_start(_registry_area, True, True, 6)

    box.add(_file_note)
    for _ in _boxes:
      box.add(_)
    return box

  def build_page1_file_read(self, m):
    _f = Frame.new(m._('Read remote file'))
    _file_read_area_opts = Box(orientation=VERTICAL, spacing=6)

    _row1 = Box()
    m._file_read_area_file_read_btn.connect('clicked', self._handlers.read_dumped_file)

    _row1.pack_start(m._file_read_area_file_read_ckbtn, False, True, 5)
    _row1.pack_start(m._file_read_area_file_read_entry, True, True, 0)
    _row1.pack_start(m._file_read_area_file_read_btn, False, True, 5)

    _file_read_area_opts.pack_start(_row1, False, True, 5)

    _f.add(_file_read_area_opts)
    return _f

  def build_page1_file_write(self, m):
    _f = Frame.new(m._('Upload local file'))
    _boxes = [Box() for _ in range(3)]

    m._file_write_area_shared_lib_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._file_write_area_shared_lib_entry]
    )

    _boxes[0].pack_start(m._file_write_area_udf_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._file_write_area_shared_lib_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._file_write_area_shared_lib_entry, True, True, 0)
    _boxes[0].pack_start(m._file_write_area_shared_lib_chooser, False, True, 5)

    m._file_write_area_file_write_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._file_write_area_file_write_entry]
    )

    _boxes[1].pack_start(m._file_write_area_file_write_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._file_write_area_file_write_entry, True, True, 0)
    _boxes[1].pack_start(m._file_write_area_file_write_chooser, False, True, 5)

    _boxes[2].pack_start(m._file_write_area_file_dest_ckbtn, False, True, 5)
    _boxes[2].pack_start(m._file_write_area_file_dest_entry, True, True, 5)

    _file_write_area_opts = Box(orientation=VERTICAL, spacing=6)
    for _ in _boxes:
      _file_write_area_opts.pack_start(_, False, True, 5)

    _f.add(_file_write_area_opts)
    return _f

  def build_page1_file_os_access(self, m):
    _f = Frame.new(m._('Access to the OS behind the DBMS'))
    _boxes = [Box() for _ in range(3)]

    _boxes[0].pack_start(m._os_access_area_os_cmd_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._os_access_area_os_cmd_entry, True, True, 5)

    _for_msf_label = label(label = m._('with Meterpreter(TCP connect):'),
                           margin_start = 50)

    _boxes[1].pack_start(m._os_access_area_os_shell_ckbtn, False, True, 5)
    _boxes[1].pack_start(_for_msf_label, False, True, 5)
    _boxes[1].pack_start(m._os_access_area_os_pwn_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._os_access_area_os_smbrelay_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._os_access_area_os_bof_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._os_access_area_priv_esc_ckbtn, False, True, 5)

    m._os_access_area_msf_path_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._os_access_area_msf_path_entry, 'choose local Metasploit install path']
    )

    _boxes[2].pack_start(m._os_access_area_msf_path_ckbtn, False, True, 5)
    _boxes[2].pack_start(m._os_access_area_msf_path_entry, True, True, 0)
    _boxes[2].pack_start(m._os_access_area_msf_path_chooser, False, True, 5)
    _boxes[2].pack_start(m._os_access_area_tmp_path_ckbtn, False, True, 5)
    _boxes[2].pack_start(m._os_access_area_tmp_path_entry, True, True, 5)

    _os_access_area_opts = Box(orientation=VERTICAL, spacing=6)
    for _ in _boxes:
      _os_access_area_opts.add(_)

    _f.add(_os_access_area_opts)
    return _f

  def build_page1_file_os_registry(self, m):
    _f = Frame.new(m._('Access to register in remote WIN'))
    _boxes = [Box() for _ in range(3)]

    m._registry_area_reg_combobox.append('--reg-read', m._('read'))
    m._registry_area_reg_combobox.append('--reg-add', m._('add'))
    m._registry_area_reg_combobox.append('--reg-del', m._('delete'))
    m._registry_area_reg_combobox.set_active(0)

    _boxes[0].pack_start(m._registry_area_reg_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._registry_area_reg_combobox, False, True, 5)
    _boxes[1].pack_start(m._registry_area_reg_key_label, False, True, 5)
    _boxes[1].pack_start(m._registry_area_reg_key_entry, True, True, 5)
    _boxes[1].pack_start(m._registry_area_reg_value_label, False, True, 5)
    _boxes[1].pack_start(m._registry_area_reg_value_entry, True, True, 5)
    _boxes[2].pack_start(m._registry_area_reg_data_label, False, True, 5)
    _boxes[2].pack_start(m._registry_area_reg_data_entry, True, True, 5)
    _boxes[2].pack_start(m._registry_area_reg_type_label, False, True, 5)
    _boxes[2].pack_start(m._registry_area_reg_type_entry, True, True, 5)

    _registry_area_opts = Box(orientation=VERTICAL)
    for _ in _boxes:
      _registry_area_opts.add(_)

    _f.add(_registry_area_opts)
    return _f

  def build_page1_other(self):
    box = Box(orientation=VERTICAL)

    _row1, _row2 = (Box(), Box())
    _page1_other_general_area = self.build_page1_other_general(self.m)
    _page1_other_misc_area = self.build_page1_other_misc(self.m)

    _row1.pack_start(_page1_other_general_area, True, True, 5)
    _row2.pack_start(_page1_other_misc_area, True, True, 5)

    box.add(_row1)
    box.add(_row2)
    return box

  def build_page1_other_general(self, m):
    _f = Frame.new(m._('General'))
    _boxes = [Box() for _ in range(11)]
    i = 0
    _boxes[i].pack_start(m._general_area_check_internet_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_fresh_queries_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_forms_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_parse_errors_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._misc_area_cleanup_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_base64_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_base64_entry, False, True, 5)
    _boxes[i].pack_start(m._general_area_base64_safe_ckbtn, False, True, 5)

    m._general_area_preprocess_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._general_area_preprocess_entry]
    )
    i += 1
    _boxes[i].pack_start(m._general_area_table_prefix_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_table_prefix_entry, False, True, 5)
    _boxes[i].pack_start(m._general_area_binary_fields_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_binary_fields_entry, False, True, 5)
    i += 1
    _boxes[i].pack_start(m._general_area_preprocess_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_preprocess_entry, True, True, 0)
    _boxes[i].pack_start(m._general_area_preprocess_chooser, False, True, 5)
    _boxes[i].pack_start(m._general_area_postprocess_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_postprocess_entry, True, True, 0)
    _boxes[i].pack_start(m._general_area_postprocess_chooser, False, True, 5)
    i += 1
    _boxes[i].pack_start(m._general_area_charset_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_charset_entry, True, True, 5)
    _boxes[i].pack_start(m._general_area_encoding_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_encoding_entry, False, True, 5)

    m._general_area_scope_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._general_area_scope_entry]
    )
    i += 1
    _boxes[i].pack_start(m._general_area_web_root_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_web_root_entry, True, True, 5)
    _boxes[i].pack_start(m._general_area_scope_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_scope_entry, True, True, 0)
    _boxes[i].pack_start(m._general_area_scope_chooser, False, True, 5)
    i += 1
    _boxes[i].pack_start(m._general_area_test_filter_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_test_filter_entry, True, True, 5)
    _boxes[i].pack_start(m._general_area_test_skip_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_test_skip_entry, True, True, 5)

    m._general_area_crawl_entry.set_width_chars(5)

    i += 1
    _boxes[i].pack_start(m._general_area_crawl_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_crawl_entry, False, True, 5)
    _boxes[i].pack_start(m._general_area_crawl_exclude_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_crawl_exclude_entry, True, True, 5)
    i += 1
    _boxes[i].pack_start(g.Separator.new(HORIZONTAL), True, True, 5)

    m._general_area_traffic_file_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._general_area_traffic_file_entry]
    )

    m._general_area_har_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._general_area_har_entry]
    )
    i += 1
    _boxes[i].pack_start(m._general_area_traffic_file_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_traffic_file_entry, True, True, 0)
    _boxes[i].pack_start(m._general_area_traffic_file_chooser, False, True, 5)
    _boxes[i].pack_start(m._general_area_har_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_har_entry, True, True, 0)
    _boxes[i].pack_start(m._general_area_har_chooser, False, True, 5)

    m._general_area_save_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._general_area_save_entry]
    )

    m._general_area_flush_session_ckbtn.get_children()[0].set_use_markup(True)
    i += 1
    _boxes[i].pack_start(m._general_area_flush_session_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_dump_format_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_dump_format_entry, False, True, 5)
    _boxes[i].pack_start(m._general_area_csv_del_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_csv_del_entry, False, True, 5)
    _boxes[i].pack_start(m._general_area_save_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_save_entry, True, True, 0)
    _boxes[i].pack_start(m._general_area_save_chooser, False, True, 5)

    m._general_area_session_file_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._general_area_session_file_entry]
    )

    m._general_area_output_dir_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._general_area_output_dir_entry, 'choose output dir']
    )
    i += 1
    _boxes[i].pack_start(m._general_area_session_file_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_session_file_entry, True, True, 0)
    _boxes[i].pack_start(m._general_area_session_file_chooser, False, True, 5)
    _boxes[i].pack_start(m._general_area_output_dir_ckbtn, False, True, 5)
    _boxes[i].pack_start(m._general_area_output_dir_entry, True, True, 0)
    _boxes[i].pack_start(m._general_area_output_dir_chooser, False, True, 5)

    _page1_other_general_opts = Box(orientation=VERTICAL, spacing=6)
    for _ in _boxes:
      _page1_other_general_opts.add(_)

    _f.add(_page1_other_general_opts)
    return _f

  def build_page1_other_misc(self, m):
    _f = Frame.new(m._('Misc'))
    _boxes = [Box() for _ in range(5)]

    m._misc_area_purge_ckbtn.get_children()[0].set_use_markup(True)

    _boxes[0].pack_start(m._misc_area_skip_heuristics_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._misc_area_skip_waf_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._misc_area_unstable_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._misc_area_list_tampers_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._misc_area_sqlmap_shell_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._misc_area_disable_color_ckbtn, False, True, 5)
    _boxes[0].pack_start(m._general_area_eta_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._misc_area_gpage_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._misc_area_gpage_spinbtn, False, True, 5)
    _boxes[1].pack_start(m._misc_area_beep_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._misc_area_offline_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._misc_area_purge_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._misc_area_dependencies_ckbtn, False, True, 5)
    _boxes[1].pack_start(m._misc_area_update_ckbtn, False, True, 5)

    m._misc_area_tmp_dir_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._misc_area_tmp_dir_entry, 'choose temp dir']
    )
    _boxes[2].pack_start(m._misc_area_alert_ckbtn, False, True, 5)
    _boxes[2].pack_start(m._misc_area_alert_entry, True, True, 5)
    _boxes[2].pack_start(m._misc_area_tmp_dir_ckbtn, False, True, 5)
    _boxes[2].pack_start(m._misc_area_tmp_dir_entry, True, True, 0)
    _boxes[2].pack_start(m._misc_area_tmp_dir_chooser, False, True, 5)
    _boxes[3].pack_start(m._misc_area_answers_ckbtn, False, True, 5)
    _boxes[3].pack_start(m._misc_area_answers_entry, True, True, 5)
    _boxes[3].pack_start(m._misc_area_z_ckbtn, False, True, 5)
    _boxes[3].pack_start(m._misc_area_z_entry, True, True, 5)

    m._misc_area_results_file_chooser.connect(
      'clicked',
      self._handlers.set_file_entry_text,
      [m._misc_area_results_file_entry]
    )
    _boxes[4].pack_start(m._misc_area_results_file_ckbtn, False, True, 5)
    _boxes[4].pack_start(m._misc_area_results_file_entry, True, True, 0)
    _boxes[4].pack_start(m._misc_area_results_file_chooser, False, True, 5)

    _page1_other_misc_opts = Box(orientation=VERTICAL, spacing=6)
    for _ in _boxes:
      _page1_other_misc_opts.add(_)

    _f.add(_page1_other_misc_opts)
    return _f

  def build_page1_tamper(self, m):
    grid = g.Grid(row_spacing = 6, margin = 15)

    _i = 0  # row number
    for a_tamper, discribe in m.tampers.items():
      if _i % 2 != 0:
        # stripe style for css
        # a_tamper.set_name('stripe')
        discribe.set_name('stripe')

      grid.attach(a_tamper, 0, _i, 1, 1)
      # grid.attach(discribe, 1, _i, 1, 1)
      _ = Box()     # resolve that label always be center align...
      _.pack_start(discribe, False, True, 0)
      grid.attach_next_to(_, a_tamper, g.PositionType.RIGHT, 1, 1)
      _i += 1

    scrolled = g.ScrolledWindow()
    scrolled.set_policy(g.PolicyType.AUTOMATIC, g.PolicyType.ALWAYS)
    scrolled.add(grid)
    return scrolled


def main():
  import time
  from widgets import d
  from model import Model
  from handlers import Handler
  from session import load_settings

  start = time.process_time()
  # --------
  win = g.Window(title = 'options-gtk')

  css_provider = g.CssProvider.new()
  css_provider.load_from_path('static/css.css')
  g.StyleContext.add_provider_for_screen(
    d.Screen.get_default(),
    css_provider,
    g.STYLE_PROVIDER_PRIORITY_APPLICATION
  )

  m = Model(load_settings()[0])
  _ = Notebook(m, Handler(win, m))
  win.add(_)

  win.connect('destroy', g.main_quit)
  win.show_all()
  # --------
  end = time.process_time()
  print('loading cost: %.3f Seconds' % (end - start))
  g.main()


if __name__ == '__main__':
  main()
