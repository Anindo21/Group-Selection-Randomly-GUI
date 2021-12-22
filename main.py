import wx
import wx.grid as grid
import os
from random_select import *
from pdf import *
from enum import Enum

# colour in HEX
buttons = wx.Colour( 246, 128, 36 ) #RGB
background = wx.Colour( 251, 226, 10 ) #RGB
other_boxes = wx.Colour( 0, 128, 230 ) #RGB
grid_label = wx.Colour( 0, 166, 228 )
grid_text = wx.Colour( 150, 217, 235 )


# Enum Class for group selection
class GroupName(Enum):
    A = 1
    B = 2
    C = 3
    D = 4


class Groups(wx.Panel):
    def __init__(self, parent, *args, **kwds):
        # begin Groups.__init__
        kwds["style"] = kwds.get("style", 0)

        wx.Panel.__init__(self, parent, *args, **kwds)

        self.SetMinSize((480, 160))

        self.parent = parent

        # the grid to make tables
        self.mygrid = grid.Grid(self)

        # initially in radiobox the group number is 2 chosen. here groupNr variable is for how many columns we have initially
        groupNr = int(self.parent.radio_box.GetString(self.parent.radio_box.GetSelection()))
        self.mygrid.CreateGrid(0, groupNr)  # creating the table of nx2 size where n is the size of list x or y

        # for naming the columns as x and y
        self.mygrid.SetColLabelValue(0, 'Group A')
        self.mygrid.SetColLabelValue(1, 'Group B')

        # set the back ground color of the row and column label
        self.mygrid.SetLabelBackgroundColour(grid_label)

        # to remove the label of the rows
        self.mygrid.SetRowLabelSize(0)

        self.mygrid.AutoSize()
        self.mygrid.EnableEditing(False)
        self.mygrid.DisableDragColSize()
        self.mygrid.DisableDragRowSize()

        self.Layout()

# end of class Groups


class MainPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin MainPanel.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Panel.__init__(self, *args, **kwds)

        # set the background color
        self.SetBackgroundColour( background )

        self.teams = []
        self.copy_teams = [] # for copying the teams in order to save
        self.dict_groups = {} # dictionary for groups
        self.N = 0 # for length of self.teams array. means number of total teams
        self.groupNr = 0  # to calculate group 1, 2, ... and start again from 1, 2, ... in generate button
        # this variable to add the team name in each group one by one
        self.groupCol = 0  # for column in table
        self.teamRow = 0  # for row in table
        self.char = 67  # start whith 'C' because the ord(67) = C
        self.c = 65 # this one needed for inserting Group A, B, C, .... in dictionary as a key, to save for pdf groups
        self.count_for_teams = 1 # this variable is needed in generate function when when we choose teams one by one and its monitor whether the group counts exists the selection of total number of groups
        self.working_directory = os.getcwd() # to get the current working directory

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(top_sizer, 0, wx.EXPAND, 0)

        top_left_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer.Add(top_left_sizer, 0, wx.EXPAND, 0)

        top_left_upper_sizer = wx.BoxSizer(wx.VERTICAL)
        top_left_sizer.Add(top_left_upper_sizer, 0, wx.EXPAND, 0)

        teams_add_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_left_upper_sizer.Add(teams_add_sizer, 0, wx.EXPAND, 0)

        team_name = wx.StaticText(self, wx.ID_ANY, "Team Name")
        teams_add_sizer.Add(team_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.txt_add_team_name = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txt_add_team_name.SetMinSize((220, -1))
        self.txt_add_team_name.SetBackgroundColour( other_boxes )
        teams_add_sizer.Add(self.txt_add_team_name, 0, wx.ALL, 4)

        self.btn_team_name = wx.Button(self, wx.ID_ANY, "Add")
        self.btn_team_name.SetBackgroundColour( buttons )
        teams_add_sizer.Add(self.btn_team_name, 0, wx.ALL, 4)

        import_teams_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_left_upper_sizer.Add(import_teams_sizer, 0, wx.EXPAND, 0)

        from_file = wx.StaticText(self, wx.ID_ANY, "Teams Choose from File")
        import_teams_sizer.Add(from_file, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        import_teams_sizer.Add((60, 20), 0, 0, 0)

        self.btn_import = wx.Button(self, wx.ID_ANY, "Import")
        self.btn_import.SetBackgroundColour( buttons )
        import_teams_sizer.Add(self.btn_import, 0, wx.ALL, 4)

        radiobox_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_left_upper_sizer.Add(radiobox_sizer, 0, wx.EXPAND, 0)

        group_nr = wx.StaticText(self, wx.ID_ANY, "Number of Groups")
        radiobox_sizer.Add(group_nr, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        radiobox_sizer.Add((60, 20), 0, 0, 0)

        self.radio_box = wx.RadioBox(self, wx.ID_ANY, "", choices=["2", "3", "4"], majorDimension=1, style=wx.RA_SPECIFY_COLS)
        self.radio_box.SetSelection(0)
        self.radio_box.SetBackgroundColour( other_boxes )
        radiobox_sizer.Add(self.radio_box, 0, wx.ALL, 4)

        combobox_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_left_upper_sizer.Add(combobox_sizer, 0, wx.EXPAND, 0)

        select_mode = wx.StaticText(self, wx.ID_ANY, "Select Mode")
        combobox_sizer.Add(select_mode, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        combobox_sizer.Add((60, 20), 0, 0, 0)

        self.combo_box = wx.ComboBox(self, wx.ID_ANY, choices=["One by One", "All in One"], style=wx.CB_DROPDOWN)
        self.combo_box.SetSelection(0)
        self.combo_box.SetBackgroundColour( other_boxes )
        combobox_sizer.Add(self.combo_box, 0, wx.ALL, 4)

        directory_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_left_upper_sizer.Add(directory_sizer, 0, wx.EXPAND, 0)

        select_mode = wx.StaticText(self, wx.ID_ANY, "Current Directory")
        directory_sizer.Add(select_mode, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        directory_sizer.Add((10, 0), 0, 0, 0)

        self.directory = wx.DirPickerCtrl(self, id=wx.ID_ANY, path=self.working_directory, message="Choose a directory to save", size=(250,-1), style=wx.DIRP_DEFAULT_STYLE | wx.DIRP_SMALL)
        directory_sizer.Add(self.directory, 0, wx.ALL, 4)

        top_left_below_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_left_sizer.Add(top_left_below_sizer, 0, wx.EXPAND, 0)

        self.btn_generate = wx.Button(self, wx.ID_ANY, "Generate Teams")
        self.btn_generate.SetBackgroundColour( buttons )
        top_left_below_sizer.Add(self.btn_generate, 0, wx.ALL, 4)

        self.btn_remove = wx.Button(self, wx.ID_ANY, "Remove Teams")
        self.btn_remove.Enable(False)
        self.btn_remove.SetBackgroundColour( buttons )
        top_left_below_sizer.Add(self.btn_remove, 0, wx.ALL, 4)

        top_sizer.Add((20, 20), 0, 0, 0)

        top_right_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer.Add(top_right_sizer, 1, wx.EXPAND, 0)

        team_names = wx.StaticText(self, wx.ID_ANY, "Team Names:")
        top_right_sizer.Add(team_names, 0, 0, 0)

        self.txt_team_names = wx.ListBox(self, id=wx.ID_ANY, choices=[], style=wx.LB_SINGLE|wx.LB_NEEDED_SB)
        self.txt_team_names.SetMinSize((420, -1))
        self.txt_team_names.SetBackgroundColour( other_boxes )
        top_right_sizer.Add(self.txt_team_names, 1, 0, 0)

        below_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(below_sizer, 0, wx.EXPAND, 0)

        below_sizer.Add((5, 0), 0, 0, 0)

        self.groups = Groups(self, wx.ID_ANY)
        below_sizer.Add(self.groups, 0, wx.EXPAND, 0)

        below_sizer.Add((252, 0), 0, 0, 0)

        button_sizer = wx.BoxSizer(wx.VERTICAL)
        below_sizer.Add(button_sizer, 0, wx.EXPAND, 0)

        self.btn_new = wx.Button(self, wx.ID_ANY, "New")
        self.btn_new.SetBackgroundColour( buttons )
        button_sizer.Add(self.btn_new, 0, wx.ALL, 4)

        self.btn_save = wx.Button(self, wx.ID_ANY, "Save")
        self.btn_save.SetBackgroundColour( buttons )
        button_sizer.Add(self.btn_save, 0, wx.ALL, 4)

        button_sizer.Add((0, 70), 0, 0, 0)

        self.btn_exit = wx.Button(self, wx.ID_ANY, "Exit")
        self.btn_exit.SetBackgroundColour( buttons )
        button_sizer.Add(self.btn_exit, 0, wx.ALL, 4)

        self.SetSizer(main_sizer)

        self.Layout()

        self.Bind(wx.EVT_TEXT, self.onTxtAddTeamName, self.txt_add_team_name)
        self.Bind(wx.EVT_BUTTON, self.onBtnAdd, self.btn_team_name)
        self.Bind(wx.EVT_BUTTON, self.onBtnImport, self.btn_import)
        self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, self.radio_box)
        self.Bind(wx.EVT_COMBOBOX, self.onComboBox, self.combo_box)
        self.Bind(wx.EVT_DIRPICKER_CHANGED, self.onDirectory, self.directory)
        self.Bind(wx.EVT_BUTTON, self.onBtnGenerate, self.btn_generate)
        self.Bind(wx.EVT_BUTTON, self.onBtnRemove, self.btn_remove)
        self.Bind(wx.EVT_LISTBOX, self.onTxtTeamNames, self.txt_team_names)
        self.Bind(wx.EVT_BUTTON, self.onBtnNew, self.btn_new)
        self.Bind(wx.EVT_BUTTON, self.onBtnSave, self.btn_save)
        self.Bind(wx.EVT_BUTTON, self.onBtnExit, self.btn_exit)

    def onTxtAddTeamName(self, event):
        ev = event.GetEventObject()
        event.Skip()

    def onBtnAdd(self, event):
        """When clicked on Add button the name of the teams written in the text ctrl will be displayed in the list box"""
        # empty string is not allowed
        if self.txt_add_team_name.GetLineText(0) != "":
            self.txt_team_names.InsertItems([self.txt_add_team_name.GetLineText(0)], self.txt_team_names.GetCount())
            self.teams.append(self.txt_add_team_name.GetLineText(0))
            self.txt_add_team_name.SetLabel("")

            self.N = len(self.teams) # to save the total number of teams
        event.Skip()

    def onBtnImport(self, event):
        """To import team names from a text file to the list box"""
        fdlg = wx.FileDialog(self, message="Choose a .txt file", defaultDir="", wildcard="(*.txt)|*.txt", style=wx.FD_DEFAULT_STYLE)
        if fdlg.ShowModal() == wx.ID_OK:
            with open(fdlg.GetPath(), "r") as fp:
                for f in fp:
                    self.txt_team_names.InsertItems([f], self.txt_team_names.GetCount())
                    self.teams.append(f.strip("\n"))

                self.N = len(self.teams)  # to save the total number of teams
        event.Skip()

    def onRadioBox(self, event):
        """To choose how many groups one needed. When a option is chosen the group number and name will be changed accordingly"""
        ev = event.GetEventObject()

        # for group no of 2
        if ev.GetSelection() == 0:
            if self.groups.mygrid.GetNumberCols() > int(ev.GetString(ev.GetSelection())):
                tot_col = self.groups.mygrid.GetNumberCols()

                while tot_col != int(ev.GetString(ev.GetSelection())):
                    tot_col -= 1
                    self.char -= 1
                    self.groups.mygrid.DeleteCols(pos=tot_col, numCols=1)
                    self.groups.mygrid.AutoSize()

        # for group no of 3
        if ev.GetSelection() == 1:
            if self.groups.mygrid.GetNumberCols() < int(ev.GetString(ev.GetSelection())):
                tot_col = self.groups.mygrid.GetNumberCols()

                while tot_col != int(ev.GetString(ev.GetSelection())):
                    self.groups.mygrid.AppendCols(numCols=1)

                    # for naming the columns as x and y
                    self.groups.mygrid.SetColLabelValue(tot_col, 'Group '+chr(self.char))
                    self.groups.mygrid.AutoSize()

                    self.char += 1
                    tot_col += 1

            if self.groups.mygrid.GetNumberCols() > int(ev.GetString(ev.GetSelection())):
                tot_col = self.groups.mygrid.GetNumberCols()

                while tot_col != int(ev.GetString(ev.GetSelection())):
                    tot_col -= 1
                    self.char -= 1
                    self.groups.mygrid.DeleteCols(pos=tot_col, numCols=1)
                    self.groups.mygrid.AutoSize()

        # for group no of 4
        if ev.GetSelection() == 2:
            if self.groups.mygrid.GetNumberCols() < int(ev.GetString(ev.GetSelection())):
                tot_col = self.groups.mygrid.GetNumberCols()

                while tot_col != int(ev.GetString(ev.GetSelection())):
                    self.groups.mygrid.AppendCols(numCols=1)

                    # for naming the columns as x and y
                    self.groups.mygrid.SetColLabelValue(tot_col, 'Group '+chr(self.char))
                    self.groups.mygrid.AutoSize()

                    self.char += 1
                    tot_col += 1

        event.Skip()

    def onComboBox(self, event):
        ev = event.GetEventObject()
        event.Skip()

    def onDirectory(self, event):
        """to select the current directory and stroe them in the current directory variable"""
        ev = event.GetEventObject()
        path = ev.GetPath()
        ev.SetPath(path)
        self.working_directory = path

        event.Skip()

    def onBtnGenerate(self, event):
        """calling random_select module Choice class to calculate or draw the random groups per teams"""
        ev = event.GetEventObject()
        # copy the teams from self.teams list
        if not self.copy_teams:
            self.copy_teams = self.teams.copy()

        if self.teams:
            # disable the data
            self.txt_add_team_name.Enable(False)
            self.btn_team_name.Enable(False)
            self.btn_import.Enable(False)
            self.radio_box.Enable(False)
            self.combo_box.Enable(False)

            # also disable the list box
            self.txt_team_names.Enable(False)
            self.btn_remove.Enable(False)

            # calling the Choice function from random_select module
            choice = Choice(self.teams)
            choice.shuffle()

            # if Select Mode is All in One
            if self.combo_box.GetSelection() == 1:
                team = choice.choose_by_sample(int(self.radio_box.GetString(self.radio_box.GetSelection())))

                # insert the teams in dictionary
                for r in range(len(team)):
                    self.dict_groups["Group "+chr(self.c)] = team[r]
                    self.c += 1  # then goes for B, C, D, .....

                self.groups.mygrid.AppendRows(numRows=len(team[0]))

                for i in range(len(team)):
                    row = 0
                    for k in team[i]:
                        self.groups.mygrid.SetCellValue(row, i, k)
                        self.groups.mygrid.SetCellBackgroundColour(row, i, grid_text)
                        self.groups.mygrid.AutoSize()
                        row += 1
                ev.Enable(False)

            # if Select Mode is One by One
            else:
                # if the list is not made before then make an empty list in the dict
                if "Group "+chr(self.c) not in self.dict_groups.keys():
                    self.dict_groups["Group "+chr(self.c)] = []

                team = choice.choose_by_team_group()

                # insert in dict the team name as list
                self.dict_groups["Group " + chr(self.c)].append(team)
                self.c += 1
                self.count_for_teams += 1
                # if self.c crosses the group limits then initialize it with beginning 'A'
                if self.count_for_teams > int(self.radio_box.GetString(self.radio_box.GetSelection())):
                    self.c = 65
                    self.count_for_teams = 1

                # to delete the teams from array
                self.teams.remove(team)

                self.groupNr += 1
                # when the group nr crosses the group numbers from radio box then initialize it as 1
                if self.groupNr > int(self.radio_box.GetString(self.radio_box.GetSelection())):
                    self.groupNr = 1

                # to show message box each time when generate button is clicked each time and show the group name by calling the enum class
                wx.MessageBox(f"Group {GroupName(self.groupNr).name}: {team}", "Result", wx.ICON_INFORMATION)

                # when total column is equal to group number chosen in radio box
                if self.groupCol == int(self.radio_box.GetString(self.radio_box.GetSelection())):
                    self.groupCol = 0  # to come to first column
                    self.teamRow += 1  # to go to next row

                # to add teams in group table
                if self.groupCol == 0:
                    # append row after completing all the columns
                    self.groups.mygrid.AppendRows(numRows=1)
                self.groups.mygrid.SetCellValue(self.teamRow, self.groupCol, team)
                self.groups.mygrid.SetCellBackgroundColour(self.teamRow, self.groupCol, grid_text)
                self.groups.mygrid.SetCellBackgroundColour(self.teamRow, self.groupCol+1, background)
                self.groups.mygrid.AutoSize()

                # if the last 2 teams left the last team will be auto inserted without pressing generate button
                if self.teamRow == (self.N // int(self.radio_box.GetString(self.radio_box.GetSelection())))-1 and self.groupCol == int(self.radio_box.GetString(self.radio_box.GetSelection()))-2:
                    self.groups.mygrid.SetCellValue(self.teamRow, self.groupCol+1, self.teams[-1])
                    self.groups.mygrid.SetCellBackgroundColour(self.teamRow, self.groupCol+1, grid_text)
                    self.groups.mygrid.AutoSize()
                    self.dict_groups["Group " + chr(self.c)].append(self.teams[-1])
                    ev.Enable(False)

                self.groupCol += 1  # go to the next column
        else:
            wx.MessageBox("Add or Import Teams First!", "Warning", wx.ICON_WARNING)

        event.Skip()

    def onBtnRemove(self, event):
        """this is to remove the teams name from list box after selecting the name"""
        ev = event.GetEventObject()
        if self.txt_team_names.IsSelected(self.txt_team_names.GetSelection()):
            # also delete from array
            self.teams.remove(self.txt_team_names.GetString(self.txt_team_names.GetSelection()).strip("\n"))

            # delete from list box
            self.txt_team_names.Delete(self.txt_team_names.GetSelection())

        ev.Enable(False)
        event.Skip()

    def onTxtTeamNames(self, event):
        """when a label is selected then the remove button will be enabled"""
        ev = event.GetEventObject()
        if ev.IsSelected(ev.GetSelection()):
            self.btn_remove.Enable(True)

        event.Skip()

    def onBtnNew(self, event):
        """to make a new entry for new draw"""
        # initialize the variables
        self.teams.clear()
        self.copy_teams.clear()
        self.dict_groups.clear()
        self.groupNr = 0
        self.char = 67
        self.c = 65
        self.count_for_teams = 1
        self.groupCol = 0
        self.teamRow = 0

        # enable the list box
        self.txt_team_names.Enable(True)

        # to delete all entry from list box
        self.txt_team_names.Clear()

        # enable the data and initialize
        self.txt_add_team_name.Enable(True)
        self.txt_add_team_name.SetLabel("")
        self.btn_team_name.Enable(True)
        self.btn_import.Enable(True)
        self.radio_box.Enable(True)
        self.radio_box.SetSelection(0)
        self.combo_box.Enable(True)
        self.combo_box.SetSelection(0)

        # enable the Generate button
        self.btn_generate.Enable(True)

        # for the table
        # clear all the entries in table
        self.groups.mygrid.ClearGrid()
        # delete all the rows
        for _ in range(self.groups.mygrid.GetNumberRows()):
            self.groups.mygrid.DeleteRows(pos=0, numRows=1)
            self.groups.mygrid.AutoSize()
        # delete columns
        if self.groups.mygrid.GetNumberCols() > 2:
            n = self.groups.mygrid.GetNumberCols()
            while n != 2:
                n -= 1
                self.groups.mygrid.DeleteCols(pos=n, numCols=1)
                self.groups.mygrid.AutoSize()

        event.Skip()

    def onBtnSave(self, event):
        """to save the teams and group details as pdf"""
        try:
            pdf = PDF()

            pdf.page_setup()
            pdf.teams(self.copy_teams)
            pdf.ln(8)
            pdf.groups(self.dict_groups)
            pdf.output(os.path.join(self.working_directory, 'info.pdf'))
            wx.MessageBox("PDF Saved Successfully", "Saved", wx.OK)
        except Exception:
            return

        event.Skip()


    def onBtnExit(self, event):
        # self.Destroy()
        wx.Exit()
        event.Skip()

# end of class MainPanel


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        wx.Frame.__init__(self, *args, **kwds)
        # to set the icon
        icon = wx.Icon() #wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap("icon.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        self.SetSize((840, 455))
        self.SetTitle("Group Selection")

        self.MainPanel = MainPanel(self, wx.ID_ANY)
        self.Layout()

# end of class MyFrame


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp


if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
