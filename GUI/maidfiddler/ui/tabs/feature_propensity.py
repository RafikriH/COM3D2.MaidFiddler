from PyQt5.QtWidgets import QListWidgetItem, QGroupBox
from PyQt5.QtCore import Qt, pyqtSignal
from .ui_tab import UiTab
from maidfiddler.util.translation import tr, tr_str


class FeaturePropensityTab(UiTab):
    feature_changed_signal = pyqtSignal(dict)
    propensity_changed_signal = pyqtSignal(dict)

    def __init__(self, ui):
        UiTab.__init__(self, ui)

        self.propensities = {}
        self.features = {}

    def update_ui(self):
        self.propensities.clear()
        self.features.clear()
        self.ui.feature_list.blockSignals(True)
        self.ui.propensity_list.blockSignals(True)
        self.ui.feature_list.clear()
        self.ui.propensity_list.clear()

        # Feature list
        for feature in self.game_data["feature_list"]:
            item = QListWidgetItem(feature["name"])
            item.setWhatsThis(f"features.{feature['name']}")
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            item.setData(Qt.UserRole, feature["id"])

            self.features[feature["id"]] = item
            self.ui.feature_list.addItem(item)

        # Propensity list

        for propensity in self.game_data["propensity_list"]:
            item = QListWidgetItem(propensity["name"])
            item.setWhatsThis(f"propensities.{propensity['name']}")
            item.setData(Qt.UserRole, propensity["id"])
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            item.setData(Qt.UserRole, propensity["id"])

            self.propensities[propensity["id"]] = item
            self.ui.propensity_list.addItem(item)

        self.ui.feature_list.blockSignals(False)
        self.ui.propensity_list.blockSignals(False)

    def init_events(self, event_poller):
        self.ui.feature_list.itemChanged.connect(self.on_feature_click)
        self.ui.propensity_list.itemChanged.connect(self.on_propensity_click)

        self.feature_changed_signal.connect(self.on_feature_change)
        self.propensity_changed_signal.connect(self.on_propensity_change)

        event_poller.on("feature_changed", self.feature_changed_signal)
        event_poller.on("propensity_changed", self.propensity_changed_signal)

    def on_feature_click(self, item):
        feature_id = item.data(Qt.UserRole)
        self.core.ToggleActiveMaidFeature(
            feature_id, item.checkState() == Qt.Checked)

    def on_propensity_click(self, item):
        propensity_id = item.data(Qt.UserRole)
        self.core.ToggleActiveMaidPropensity(
            propensity_id, item.checkState() == Qt.Checked)

    def on_feature_change(self, args):
        self.ui.feature_list.blockSignals(True)
        self.features[args["id"]].setCheckState(
            Qt.Checked if args["selected"] else Qt.Unchecked)
        self.ui.feature_list.blockSignals(False)

    def on_propensity_change(self, args):
        self.ui.propensity_list.blockSignals(True)
        self.propensities[args["id"]].setCheckState(
            Qt.Checked if args["selected"] else Qt.Unchecked)
        self.ui.propensity_list.blockSignals(False)

    def on_maid_selected(self):
        if self.maid_mgr.selected_maid is None:
            return

        maid = self.maid_mgr.selected_maid

        self.ui.feature_list.blockSignals(True)
        for f_id, item in self.features.items():
            item.setCheckState(Qt.Unchecked)
        for feat_id in maid["feature_ids"]:
            self.features[feat_id].setCheckState(Qt.Checked)
        self.ui.feature_list.blockSignals(False)

        self.ui.propensity_list.blockSignals(True)
        for p_id, item in self.propensities.items():
            item.setCheckState(Qt.Unchecked)
        for prop_id in maid["propensity_ids"]:
            self.propensities[prop_id].setCheckState(Qt.Checked)
        self.ui.propensity_list.blockSignals(False)

    def translate_ui(self):
        self.ui.ui_tabs.setTabText(2, tr(self.ui.tab_feature_propensity))

        for group in self.ui.tab_feature_propensity.findChildren(QGroupBox):
            group.setTitle(tr(group))

        self.ui.feature_list.blockSignals(True)
        for i in range(0, self.ui.feature_list.count()):
            item = self.ui.feature_list.item(i)
            item.setText(tr(item))
        self.ui.feature_list.blockSignals(False)

        self.ui.propensity_list.blockSignals(True)
        for i in range(0, self.ui.propensity_list.count()):
            item = self.ui.propensity_list.item(i)
            item.setText(tr(item))
        self.ui.propensity_list.blockSignals(False)
